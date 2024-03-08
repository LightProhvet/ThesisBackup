#!/usr/bin/env python3

"""
This node takes control when robot's location is known well enough and next destination is a point on the map
sufficiently nearby, so navigation by odometry (just checking for obstacles) is reliable enough.
Meant to be used to navigate in areas where linefollowing would be too clumsy:
- positioning the robot into waiting area in front of an elevator or door
- from waiting area to the entering position in front of elevator door
- into the elevator
- out of elevator
"""

import rclpy
from rclpy.node import Node
from rclpy.parameter import Parameter

import numpy as np
import time
import math
import tf2_ros
from std_msgs.msg import Int32, String, Bool, Int16
from geometry_msgs.msg import Vector3Stamped, Twist, TransformStamped
from robot_ros2_msgs.msg import IntList
from .Controllers import CoordNavController
from tf_transformations import euler_from_quaternion, quaternion_from_euler, quaternion_multiply
from .ObstacleAvoidanceHelpers import ObstacleAvoidanceHelpers


class CoordinateNavigator(Node):
    def __init__(self, rate):
        # Subscribers
        super().__init__('CoordinateNavigator')

        self.op_mode_sub = self.create_subscription(String, "op_mode", self.onOpMode, 10)
        self.destination_sub = self.create_subscription(String, "coordinate_destination", self.onNewDestination, 10)
        self.obst_dists_on_paths_sub = self.create_subscription(IntList, "obst_dists_on_paths", self.onObstDists, 10)

        # Publishers
        self.body_vel_cmd_pub = self.create_publisher(Twist, "/cmd_vel", 1)
        self.move_completed_pub = self.create_publisher(Bool, "coordinate_navigator_move_complete", 1)
        self.debug_path_pub = self.create_publisher(Int16, "debug_path", 0)
        self.debug_state_pub = self.create_publisher(String, "debug_state", 0)

        # Transform listener
        self.tfBuffer = tf2_ros.Buffer()
        self.listener = tf2_ros.TransformListener(self.tfBuffer, self)

        # Messages to be published
        self.body_vel_cmd_msg = Twist()

        self.obst_avoid_helpers = ObstacleAvoidanceHelpers()
        self.obst_dists_on_paths = [0, 0, 0, 0, 0, 0, 0]  # free distances at 7 visible routes, got from LineAndObstacleDetector

        self.speeds = [0, 0]
        self.controller = CoordNavController(0.25, 0.02, 0.2, 0.01, 2, 0.3, 0.2)

        self.declare_parameter("allowed_distance_difference", Parameter.Type.DOUBLE)
        self.declare_parameter("allowed_rotation_difference", Parameter.Type.DOUBLE)

        self.allowed_distance_diff = self.get_parameter("allowed_distance_difference").value
        self.allowed_rotation_diff = self.get_parameter("allowed_rotation_difference").value

        self.enabled = False
        self.TF_result_is_real = False
        self.coord_dest_name = ""
        self.tf_to_dest = TransformStamped()
        self.offset = np.zeros([3])  # X linear, y linear, Z rotational
        self.stage = 1
        self.dist_to_obst = 0
        self.path_to_drive = -1
        self.debug_state = ""

        self.rate = self.create_rate(10)
        self.timer = self.create_timer(0.1, self.run)

    def onOpMode(self, op_mode_msg):
        self.enabled = op_mode_msg.data == "coordinate_navigator"

    def onObstDists(self, obst_dists_msg):
        """
        Handles incoming info about distances that could be travelled ahead on 7 different paths in view
        """
        for i, val in enumerate(obst_dists_msg.data):
            self.obst_dists_on_paths[i] = val / 1000  # Convert from mm to m

    def onNewDestination(self, destination_msg):
        self.coord_dest_name = destination_msg.data
        self.stage = 1
        self.get_logger().info("New coordinate destination" + str(self.coord_dest_name))

    def run(self):
        """
        Main loop of class.
        @param: self
        @result: runs the step function
        """
        self.step()
        #self.rate.sleep()

    def step(self):

        self.debug_state = ""
        # When coordinate navigator gets enabled first time, it checks if the TF of world->odom is startup default that
        #   would be useless or has it been corrected by arucos and lets coordinate navigator to work okay.
        if self.enabled and not self.TF_result_is_real:
            test_tf = self.tfBuffer.lookup_transform('map', 'odom', self.get_clock())
            if test_tf.transform.translation.x != 0 and test_tf.transform.translation.y != 0:
                self.TF_result_is_real = True

        if self.coord_dest_name != "" and self.TF_result_is_real:
            # Find distance and direction of base_footprint's offset from goal coordinate
            exception = False
            try:
                self.tf_to_dest = \
                    self.tfBuffer.lookup_transform('base_footprint', self.coord_dest_name, self.get_clock())
                # self.get_logger().info("TF to destination:" + str(self.tf_to_dest.transform))
            except (tf2_ros.LookupException, tf2_ros.ConnectivityException, tf2_ros.ExtrapolationException) as e:
                exception = True
                self.get_logger().info("TF exception" + str(e))
                self.debug_state = self.debug_state + "TF exception. "

            if exception:
                self.body_vel_cmd_msg.linear.x = 0
                self.body_vel_cmd_msg.linear.y = 0
                self.body_vel_cmd_msg.angular.z = 0

            else:
                # Calculate 2D distance from goal
                distance = math.sqrt(self.tf_to_dest.transform.translation.x ** 2 + self.tf_to_dest.transform.translation.y ** 2)
                if self.tf_to_dest.transform.translation.x < 0:
                    distance = 0  # Make sure robot does not keep moving if it missed the closest point to destination.
                # Calculate Z rotation difference
                z_rotation_diff = math.atan2(self.tf_to_dest.transform.translation.y, self.tf_to_dest.transform.translation.x)
                # self.get_logger().info("z_rotation_diff:" + str(z_rotation_diff))
                # Clip rotation diff values because they tend to cause sudden moves
                if z_rotation_diff > 0.5:
                    z_rotation_diff = 0.5
                elif z_rotation_diff < -0.5:
                    z_rotation_diff = -0.5

                # Get orientation diff - needed to detect if the final rotation is right
                _x_angle, _y_angle, orientation_diff = euler_from_quaternion([
                                                            self.tf_to_dest.transform.rotation.x,
                                                            self.tf_to_dest.transform.rotation.y,
                                                            self.tf_to_dest.transform.rotation.z,
                                                            self.tf_to_dest.transform.rotation.w])

                self.path_to_drive = -1

                if self.stage == 3 and -self.allowed_rotation_diff <= orientation_diff <= self.allowed_rotation_diff:
                    # Stop motors
                    self.body_vel_cmd_msg.linear.x = 0
                    self.body_vel_cmd_msg.linear.y = 0
                    self.body_vel_cmd_msg.angular.z = 0
                    if self.enabled:
                        self.body_vel_cmd_pub.publish(self.body_vel_cmd_msg)
                        self.enabled = False  # disable the node
                    # Publish move finished
                    self.move_completed_pub.publish(True)
                    self.coord_dest_name = ""
                    self.get_logger().info("Coordinate navigation completed")

                else:

                    if self.stage == 1:  # First stage is turning camera towards the destination
                        if -self.allowed_rotation_diff < z_rotation_diff < self.allowed_rotation_diff:
                            self.stage = 2
                            if self.enabled:
                                self.get_logger().info("Coordinate nav start move stage 2, dist " + str(distance))
                        else:
                            self.speeds = self.controller.control(0, z_rotation_diff)
                            self.debug_state = self.debug_state + "Stage 1, diff=" + str("{:.2f}".format(z_rotation_diff)) + "rad. "

                    elif self.stage == 2: # Second stage is approaching the destination, if needed correct also z rotation
                        if -self.allowed_distance_diff < distance < self.allowed_distance_diff:
                            self.stage = 3
                            if self.enabled:
                                self.get_logger().info("Coordinate nav start move stage 3")
                        else:
                            best_direction = self.obst_avoid_helpers.findBestDirectionFromAngle(z_rotation_diff)
                            self.path_to_drive = self.obst_avoid_helpers.findPathToDrive(best_direction,
                                                                                     self.obst_dists_on_paths, 0.2)
                            if self.path_to_drive != -1:
                                self.speeds = self.obst_avoid_helpers.controlSpeedsByPathToDrive(
                                    self.obst_dists_on_paths[self.path_to_drive],
                                    self.path_to_drive)

                            else:
                                self.speeds = [0, 0]

                            if self.enabled:
                                self.get_logger().info("dist" + str(distance))
                            self.debug_state = self.debug_state + "Stage 2, dist=" + str(
                                "{:.2f}".format(z_rotation_diff)) + ". "


                    else: # Third stage is rotating into position
                        self.speeds = self.controller.control(0, orientation_diff)
                        self.debug_state = self.debug_state + "Stage 3, diff=" + str("{:.2f}".format(orientation_diff)) + "rad. "

                    # Assemble move command
                    self.body_vel_cmd_msg.linear.x = self.speeds[0]
                    self.body_vel_cmd_msg.linear.y = 0
                    self.body_vel_cmd_msg.angular.z = self.speeds[1]

        elif self.enabled and not self.TF_result_is_real:
            self.get_logger().info("Robot location not confirmed by Arucos, coordinate navigation impossible.")

        if self.enabled:
            self.body_vel_cmd_pub.publish(self.body_vel_cmd_msg)
            if not self.TF_result_is_real: # Send a little info to console when can't move bacause of lack of info.
                self.get_logger().info("Coordinate navigator can't navigate because robot location has not been confirmed from Arucos.")
            self.debug_state_pub.publish(self.debug_state)
            self.debug_path_pub.publish(self.path_to_drive)

def main(args=None):
    rclpy.init(args=args)
    node = CoordinateNavigator(10)
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()