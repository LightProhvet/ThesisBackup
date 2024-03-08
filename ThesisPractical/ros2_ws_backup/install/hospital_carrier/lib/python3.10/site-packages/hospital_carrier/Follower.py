#!/usr/bin/env python3

"""
@authors: Christian Meurer, Anna J&otilde;gi
@input: -Tag information (is ast Tag reached? and 
        corrected distance from next Tag)
        -Information about obstacles (Boolean for now)
        -Manual overwrite
@output: Body velocities for the robot  
Class that computes necessary body velocities to correct for
the offsets between robot and line
"""

import rclpy
from rclpy.node import Node
from rclpy.parameter import Parameter

import numpy as np
from std_msgs.msg import Int16, String, Bool
from geometry_msgs.msg import Vector3Stamped, Twist
from robot_ros2_msgs.msg import IntList
import tf2_ros
from tf_transformations import euler_from_quaternion, quaternion_from_euler, quaternion_multiply
from .ObstacleAvoidanceHelpers import ObstacleAvoidanceHelpers
import time


class Follower(Node):
    NORMAL = "state_follower_normal"  # for linefollowing and passing obstacles while moving forward
    SCANNING_0 = "state_follower_waiting_for_opening"  # for standing still and possibly letting moving obstacle pass
    SCANNING_1 = "state_follower_scanning_for_opening_phase_1" # for just turning to a set direction and looking for opening
    SCANNING_2 = "state_follower_scanning_for_opening_phase_2"
    STUCK = "state_follower_scanning_stuck_stop" # when scanning did not give results, standing still

    def __init__(self, rate):

        super().__init__('Follower')
        
        # Subscribers
        self.op_mode_sub = self.create_subscription(String, "op_mode", self.onOpMode, 10)
        self.tag_type_sub = self.create_subscription(String, "tag_type", self.onTagType, 10)
        #self.tagdist_corr_sub = self.create_subscription(Int16, "tagdist_corr", self.onTagDist, 10)
        self.line_and_obst_sub = self.create_subscription(Vector3Stamped, "line_and_obst", self.onLineAndObst, 10)
        self.obst_dists_on_paths_sub = self.create_subscription(IntList, "obst_dists_on_paths", self.onObstDists, 10)
        self.obst_pass_side_sub = self.create_subscription(String, "obst_pass_side", self.onObstPassSide, 10)

        # parameters
        self.declare_parameter("vel_x_const", Parameter.Type.DOUBLE)
        self.declare_parameter("gain_type", Parameter.Type.STRING)

        self.vel_x_const = self.get_parameter("vel_x_const").value
        self.gain_type = self.get_parameter("gain_type").value

        # Publishers
        self.body_vel_cmd_pub = self.create_publisher(Twist, "/cmd_vel", 1)
        self.debug_line_sector_pub = self.create_publisher(Int16, "debug_line_sector", 1)
        self.debug_path_pub = self.create_publisher(Int16, "debug_path", 1)
        self.debug_state_pub = self.create_publisher(String, "debug_state", 1)

        # Messages to be published
        self.body_vel_cmd_msg = Twist()

        # Transform listener
        self.tfBuffer = tf2_ros.Buffer()
        self.listener = tf2_ros.TransformListener(self.tfBuffer, self)

        # define vector for body distance offset
        self.offset = np.zeros([3])

        self.obst_avoid_helpers = ObstacleAvoidanceHelpers()

        self.enabled = False
        self.state = self.NORMAL
        self.is_line = False
        self.line_dir = Int16()
        self.line_dir.data = -1
        self.line_angle = 0  # Holds line blob center's location angle in camera view (from bottom center), got from LineAndObstacleDetector
        self.future_path_dist = 0 # Holds line blob center's distance from robot, got from LineAndObstacle detector. Currently not in use.
        self.obst_dists_on_paths = [0, 0, 0, 0, 0, 0, 0]  # free distances at 7 visible routes, got from LineAndObstacleDetector
        self.obst_pass_side = None
        self.scanning_start_angle = 0
        self.scan_dir = 1
        self.scanning_0_phase_start_time = 0
        self.scanning_0_phase_duration = 2  #how many seconds to wait for obstacle to pass on it's own before turning

        self.swivel_speed = 0.15   # Angular speed while looking for a free path for passing an obstacle
        self.scanning_1st_phase_angle = 1.57  # 90 deg in rad
        self.scanning_2nd_phase_angle = 6.28  # When to stop trying when no opening found, 360 deg in rad

        self.rate = self.create_rate(rate)
        self.timer = self.create_timer(0.1, self.run)

    def run(self):
        """
        Main loop of class.
        @param: self
        @result: runs the step function
        """
        self.step()
        #self.rate.sleep()


    def step(self):
        """
        Perform an iteration of the Follower loop.
        @param: self
        @result: updates and publishes body velocities 
        """

        # We have is_line and line_dir from LineAndObstacleDetector. Also obst_dists_on_paths. Get TF of robot base in
        #  in route_section frame also.
        tf_robot_to_route_section = None
        rotation_diff_from_section = 0
        try:
            tf_robot_to_route_section = self.tfBuffer.lookup_transform('route_section', 'base_footprint',
                                                                               self.get_clock().now())
        except (tf2_ros.LookupException, tf2_ros.ConnectivityException, tf2_ros.ExtrapolationException) as e:
            pass  # tf_robot_to_route_section = None indicates the situation

        path_to_drive = -1
        if tf_robot_to_route_section is None:  # If there is no info about the route_section
            if self.enabled:
                self.get_logger().info("No line visible, no info about robot and route locations, can't drive")
            self.body_vel_cmd_msg.linear.x = 0.0
            self.body_vel_cmd_msg.angular.z = 0.0
        else:
            _x_angle, _y_angle, rotation_diff_from_section = euler_from_quaternion([
                tf_robot_to_route_section.transform.rotation.x,
                tf_robot_to_route_section.transform.rotation.y,
                tf_robot_to_route_section.transform.rotation.z,
                tf_robot_to_route_section.transform.rotation.w])

            #self.get_logger().info("rotation_diff_from_section" + str(rotation_diff_from_section))

            # Check that the robot is not facing reverse direction for some reason
            if rotation_diff_from_section < -1.6 or rotation_diff_from_section > 1.6:
                self.is_line = False  # If it is reversed, ignore the line, wrong direction

            if self.is_line:  # If line is visible, preferred direction is it's direction
                best_direction = self.obst_avoid_helpers.findBestDirectionFromAngle(self.line_angle)
            else:
                best_direction = self.obst_avoid_helpers.findBestDirectionFromAngle(rotation_diff_from_section)

            path_to_drive = self.obst_avoid_helpers.findPathToDrive(best_direction, self.obst_dists_on_paths)

            #self.get_logger().info("path_to_drive", path_to_drive, "Obst dists", self.obst_dists_on_paths[0], self.obst_dists_on_paths[1], self.obst_dists_on_paths[2], \
            #      self.obst_dists_on_paths[3], self.obst_dists_on_paths[4], self.obst_dists_on_paths[5],
            #      self.obst_dists_on_paths[6])
            #self.get_logger().info("Is_line:", self.is_line, ", path_to_drive", path_to_drive)

            if path_to_drive == -1 and self.state == self.NORMAL:
                # Stop robot and go to pre scanning phase 0
                self.state = self.SCANNING_0
                self.scanning_0_phase_start_time = time.time()
                if self.enabled:
                    self.get_logger().info("Follower Scanning 0 - obstacle close, stand still for 2 sec")

            elif path_to_drive != -1 and self.state in [self.SCANNING_0, self.SCANNING_1, self.SCANNING_2, self.STUCK]:
                self.state = self.NORMAL
                if self.enabled:
                    self.get_logger().info("Follower back to state = NORMAL")

            elif self.state == self.SCANNING_0 and \
                    self.scanning_0_phase_start_time + self.scanning_0_phase_duration < time.time():
                self.state = self.SCANNING_1
                self.scan_dir = 1 if self.obst_pass_side == "left" else -1
                self.scanning_start_angle = rotation_diff_from_section  # TODO is this viable? Does it "overflow" after 180 deg?
                if self.enabled:
                    self.get_logger().info("Follower start state SCANNING_1")

            # Compute speeds according to state.
            if self.state == self.NORMAL:
                speeds = self.obst_avoid_helpers.controlSpeedsByPathToDrive(self.obst_dists_on_paths[path_to_drive],
                                                                                                    path_to_drive)
                # assign velocity commands to twist message
                self.body_vel_cmd_msg.linear.x = speeds[0]
                self.body_vel_cmd_msg.angular.z = speeds[1]

            elif self.state == self.SCANNING_1 or self.state == self.SCANNING_2:
                scanned_angle = 0
                if self.scan_dir == 1:
                    scanned_angle = rotation_diff_from_section - self.scanning_start_angle
                else:
                    scanned_angle = self.scanning_start_angle - rotation_diff_from_section
                # Check if the scanning phase should end
                if self.state == self.SCANNING_1 and scanned_angle > self.scanning_1st_phase_angle:
                    self.scan_dir = -1 * self.scan_dir
                    self.state = self.SCANNING_2
                    self.body_vel_cmd_msg.linear.x = 0.0
                    self.body_vel_cmd_msg.angular.z = 0.0
                    if self.enabled:
                        self.get_logger().info("Follower start state SCANNING_2")
                elif self.state == self.SCANNING_2 and scanned_angle > self.scanning_2nd_phase_angle:
                    self.state = self.STUCK
                    self.body_vel_cmd_msg.linear.x = 0.0
                    self.body_vel_cmd_msg.angular.z = 0.0
                    if self.enabled:
                        self.get_logger().info("Follower start state STUCK")
                # If in the middle of the scanning, assign velocity commands to twist message
                else:
                    self.body_vel_cmd_msg.linear.x = 0.0
                    self.body_vel_cmd_msg.angular.z = self.scan_dir * self.swivel_speed

            elif self.state == self.SCANNING_0:
                self.body_vel_cmd_msg.linear.x = 0.0
                self.body_vel_cmd_msg.angular.z = 0.0

            elif self.state == self.STUCK:
                    #Check if it's time to recheck the situation around robot
                    pass #TODO

        # if follower mode is enabled publish velocity commands as twist message
        if self.enabled:
            self.body_vel_cmd_pub.publish(self.body_vel_cmd_msg)
            # Publish state data to be shown in debug window
            #self.debug_path_pub.publish(path_to_drive)
            self.debug_state_pub.publish(self.state)
        if self.is_line:
            self.line_dir.data = self.obst_avoid_helpers.findBestDirectionFromAngle(self.line_angle)
        else:
            self.line_dir.data = -1
        self.debug_line_sector_pub.publish(self.line_dir)


    def onOpMode(self, op_mode_msg):
        self.enabled = op_mode_msg.data == "follower"
        
    def onTagType(self, tag_msg):
        """
        Handles incoming information if last Tag is reached.
        @param: self
        @param: tag_msg - Boolean indicating if last Tag or not
        @result: makes boolean globally available
        """
        self.tag_type = tag_msg

        
    def onTagDist(self, dist_msg):
        """
        Handles incoming tag distance updates.
        @param: self
        @param dist_msg - Int16 scalar for distance to
                          next tag
        @result: make tag distance messages globally available.
        """
        self.dist2tag = dist_msg

    def onLineAndObst(self, msg):
        """
        Handles incoming info about line and obstacle free area
        @param: self
        """
        self.future_path_dist = msg.vector.x
        self.line_angle = msg.vector.z

    def onObstDists(self, obst_dists_msg):
        """
        Handles incoming info about distances that could be travelled ahead on 7 different paths in view
        """
        for i, val in enumerate(obst_dists_msg.data):
            self.obst_dists_on_paths[i] = val / 1000  # Convert from mm to m

    def onObstPassSide(self, obs_pass_side_msg):
        self.obst_pass_side = obs_pass_side_msg.data

def main(args=None):
    rclpy.init(args=args)
    node = Follower(10)
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
