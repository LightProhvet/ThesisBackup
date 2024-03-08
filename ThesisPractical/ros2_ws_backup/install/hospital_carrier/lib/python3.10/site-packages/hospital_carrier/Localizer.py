#!/usr/bin/env python3

"""
@authors: Christian Meurer and Anna J&otilde;gi
@input: Tag information (Tag ID, Tag location, Floor level), TF transform of sensor_detected_base_footprint in the
world map)
@output: Specific information about the tag (last Tag, special Tag), TF transform of odom layer so that the
base_footprint aligns with the sensor_detected_base_footprint in the world map.
Class that makes up the localization node of the line following framework

@Mapping the environment: the TF tree is set up as follows:
world
  map_floor1 (static to world)
    aruco1 (static to map_floor1)
    aruco2 (static to map_floor1)
    ...
  map_floor2 (static to world)
  ...
  odom (holds the continuous line of odometry data but odom "layer"'s position is shifted in respect to world when new
                   more exact data comes in - then position of the robot in the world therefore in respect to maps
                   is adjusted by transforming the odom's coordinates)
    base_footprint
        camera_link (static to base_footprint)
----------
In addition helper entities are assigned as children of currently detected aruco tag (code in ReadAruco node)
         sensor_detected_camera_link
           sensor_detected_base_footprint (static to sensor_detected_camera_link)

"""


import rclpy
from rclpy.node import Node
from rclpy.parameter import Parameter
from std_msgs.msg import Int16, String
from geometry_msgs.msg import PoseStamped, Vector3Stamped, TransformStamped, Twist
from nav_msgs.msg import Odometry, Path

import numpy as np
import math
import time
from tf_transformations import euler_from_quaternion, quaternion_from_euler, quaternion_multiply
from robot_ros2_msgs.msg import Tag, Encoders
import tf2_ros


class Localizer(Node):
    def __init__(self, rate):

        super().__init__('Localizer')

        # Subscribers
        self.tag_sub = self.create_subscription(Tag, "arucoTag", self.onTag, 10)
        #self.encoder_sub = self.create_subscription(Encoders, "encoders", self.onEncoder, 10)
        #self.line_offset_sub = self.create_subscription(Vector3Stamped, "line_offset", self.onLine, 10)
        self.cmd_vel_ex_sub = self.create_subscription(Twist, "cmd_vel_executed", self.onVelCmdEx, 10)

        # parameters
        self.declare_parameters(namespace='', parameters=[
            ('last_tag_ID', Parameter.Type.INTEGER),
            ('elevator_tag_IDs', Parameter.Type.INTEGER_ARRAY),
            ('max_tag_distance', Parameter.Type.INTEGER),
            ('ventral_wheel_distance', Parameter.Type.DOUBLE),
            ('lateral_wheel_distance', Parameter.Type.DOUBLE),
            ('wheel_radius', Parameter.Type.DOUBLE),
            ('encoder_resolution', Parameter.Type.INTEGER),
            ('encoder_rate', Parameter.Type.DOUBLE)
        ])

        self.elevator_tag_ID = self.get_parameter("elevator_tag_IDs").value
        self.last_tag_ID = self.get_parameter("last_tag_ID").value
        self.d_ventral = self.get_parameter("ventral_wheel_distance").value
        self.d_lateral = self.get_parameter("lateral_wheel_distance").value
        self.r_wheel = self.get_parameter("wheel_radius").value
        self.max_tag_dist = self.get_parameter("max_tag_distance").value
        self.encoder_rate = self.get_parameter("encoder_rate").value

        # Publishers
        self.tag_type_pub = self.create_publisher(String, "tag_type", 25)
        #self.tagdist_corr_pub = self.create_publisher(Int16, "tagdist_corr", 25)
        self.global_pose_pub = self.create_publisher(PoseStamped, "global_pose", 25)
        self.encoder_odom_pub = self.create_publisher(Odometry, "encoder_odom", 25)
        #self.path_pub = self.create_publisher(Path, "pathFromEncoders", 10)

        # Transform listener
        self.tfBuffer = tf2_ros.Buffer()
        self.listener = tf2_ros.TransformListener(self.tfBuffer, self)
        # Transform broadcasters
        self.odom_transform_broadcaster = tf2_ros.TransformBroadcaster(self)
        self.odom_transform_msg = TransformStamped()
        self.base_transform_broadcaster = tf2_ros.TransformBroadcaster(self)
        self.base_transform_msg = TransformStamped()

        # Fill initial TF transform data
        self.odom_transform_msg.transform.translation.x = 0.0
        self.odom_transform_msg.transform.translation.y = 0.0
        self.odom_transform_msg.transform.translation.z = 0.0
        self.odom_transform_msg.transform.rotation.x = 0.0
        self.odom_transform_msg.transform.rotation.y = 0.0
        self.odom_transform_msg.transform.rotation.z = 0.0
        self.odom_transform_msg.transform.rotation.w = 1.0
        self.odom_transform_msg.header.frame_id = "map"
        self.odom_transform_msg.child_frame_id = "odom"
        self.odom_transform_msg.header.stamp = self.get_clock().now().to_msg()

        self.base_transform_msg.transform.translation.x = 0.0
        self.base_transform_msg.transform.translation.y = 0.0
        self.base_transform_msg.transform.translation.z = 0.0
        self.base_transform_msg.transform.rotation.x = 0.0
        self.base_transform_msg.transform.rotation.y = 0.0
        self.base_transform_msg.transform.rotation.z = 0.0
        self.base_transform_msg.transform.rotation.w = 1.0
        self.base_transform_msg.header.frame_id = "odom"
        self.base_transform_msg.child_frame_id = "base_footprint"
        self.base_transform_msg.header.stamp = self.get_clock().now().to_msg()


        # Messages to be published
        self.tag_type_msg = String()
        #self.tagdist_corr_msg = Int16()
        self.global_pose_msg = PoseStamped()
        self.encoder_odom_msg = Odometry()
        #self.path = Path()



        # define matrix for inverse kinematics for Mecanum wheels
        # in following oder: front_right, front_left, back_left, back_right
        a = (self.d_ventral + self.d_lateral)
        self.mec_mat = np.array([[1, 1, 1, 1], \
                                [1, -1, 1, -1], \
                                [1/a, -1/a, -1/a, 1/a]])

        # initialize variables 
        self.pose = np.zeros(6) # starting pose (x,y,floor,0,0,theta) #TODO replace with only floor data
        self.line_offset = np.zeros(2)
        self.wheel_speed = np.zeros(4)
        self.vel_body = np.zeros(3)
        self.tag_dist = 0.0
        self.current_tag = None
        self.tag_ID = None
        self.newTag = False
        self.dist_traveled = 0.0
        self.measuredPosition = np.zeros(2)
        self.new_encoder_data = False
        self.new_sensor_location_data_ready = False
        self.last_transform_stamp = [0, 0]
        self.time_vel_cmd = time.time()
        self.prev_vel_cmd = np.zeros(3)

        # EKF matrices
        self.Jacobian = np.identity(3)
        self.P = np.identity(3) * 0.001
        self.H = np.identity(3)
        self.Q = np.identity(3) * 0.001

        self.rate = self.create_rate(10)
        self.timer = self.create_timer(0.1, self.run)

    def run(self):
        """
        Main loop of class.
        @param: self
        @result: runs the step function for localizer update
        """

        # Broadcast initial odom transform, so the TF tree gets connected
        self.odom_transform_msg.header.stamp = self.get_clock().now().to_msg()
        #self.odom_transform_broadcaster.sendTransform(self.odom_transform_msg)
        self.base_transform_msg.header.stamp = self.get_clock().now().to_msg()
        #self.base_transform_broadcaster.sendTransform(self.base_transform_msg)

        if self.last_tag_ID > 0:
            self.step()
        else:
            self.get_logger().warn('tag_ID for last tag not defined')

            #self.rate.sleep()


    def step(self):
        """
        Perform an iteration of the localizer loop.
        @param: self
        @result: updates and publishes pose estimation of 
                 the vehicle globally and relative to the
                 next waypoint. Parses distance to next 
                 waypoint to the path-following node 
        """
        self.base_transform_msg.header.stamp = self.get_clock().now().to_msg()
        #self.base_transform_broadcaster.sendTransform(self.base_transform_msg)

        # check which tag is in front of us
        if self.tag_ID == self.last_tag_ID:
            self.tag_type_msg.data = "last tag"
        elif self.tag_ID == any(self.elevator_tag_ID): 
            self.tag_type_msg.data = "elevator"
        else:
            self.tag_type_msg.data = "normal tag"
        self.tag_type_pub.publish(self.tag_type_msg)

        '''
        # TODO is this needed? It seems rviz is only one using it.
        if self.new_encoder_data:
            self.dt = self.encoder_rate
            # publish encoder odometry to check if estimation is correct
            self.encoder_odom_msg.header.stamp = self.get_clock().now().to_msg()
            self.encoder_odom_msg.header.frame_id = "odom"
            self.encoder_odom_msg.child_frame_id = "base_footprint"
            self.encoder_odom_msg.pose.pose.position.x = self.pose[0]
            self.encoder_odom_msg.pose.pose.position.y = self.pose[1]
            self.encoder_odom_msg.pose.pose.position.z = self.pose[2]
            quat = quaternion_from_euler(0.0, 0.0, self.pose[5])
            self.encoder_odom_msg.pose.pose.orientation.x = quat[0]
            self.encoder_odom_msg.pose.pose.orientation.y = quat[1]
            self.encoder_odom_msg.pose.pose.orientation.z = quat[2]
            self.encoder_odom_msg.pose.pose.orientation.w = quat[3]
            self.encoder_odom_msg.twist.twist.linear.x = self.vel_body[0]
            self.encoder_odom_msg.twist.twist.linear.y = self.vel_body[1]
            self.encoder_odom_msg.twist.twist.angular.z = self.vel_body[2]
            self.encoder_odom_pub.publish(self.encoder_odom_msg)

            self.new_encoder_data = False
        '''

        # When there is new sensor_calculated_base_footprint transform available then also get transforms of
        # odom and base_footprint in the world frame.
        if self.newTag == True:
            try:
                transform_base_footprint_to_world = self.tfBuffer.lookup_transform('map' ,'base_footprint', self.get_clock().now())
                if transform_base_footprint_to_world.header.stamp.secs != self.last_transform_stamp[0] and \
                        transform_base_footprint_to_world.header.stamp.nsecs != self.last_transform_stamp[1]:
                    self.new_sensor_location_data_ready = True
                    self.last_transform_stamp[0] = transform_base_footprint_to_world.header.stamp.secs
                    self.last_transform_stamp[1] = transform_base_footprint_to_world.header.stamp.nsecs
                else:
                    self.new_sensor_location_data_ready = False
            except (tf2_ros.LookupException, tf2_ros.ConnectivityException, tf2_ros.ExtrapolationException) as e:
                pass
            try:
                transform_calculated_to_world = \
                    self.tfBuffer.lookup_transform('map', 'sensor_calculated_base_footprint', self.get_clock().now())
            except (tf2_ros.LookupException, tf2_ros.ConnectivityException, tf2_ros.ExtrapolationException) as e:
                self.new_sensor_location_data_ready = False
            try:
                transform_odom_to_world = self.tfBuffer.lookup_transform('map', 'odom', self.get_clock().now())
            except (tf2_ros.LookupException, tf2_ros.ConnectivityException, tf2_ros.ExtrapolationException) as e:
                self.new_sensor_location_data_ready = False

            # If there was new transform for sensor_calculated_base_footprint and other transforms were also gathered
            # successfully then compute a new transform for odom layer that places the base_footprint
            # to the same location in world frame where the sensor_calculated_base_footprint was.
            if self.new_sensor_location_data_ready:
                self.odom_transform_msg.header.frame_id = "map"
                self.odom_transform_msg.child_frame_id = "odom"
                self.odom_transform_msg.transform.translation.x = transform_odom_to_world.transform.translation.x + \
                                                             transform_calculated_to_world.transform.translation.x - \
                                                             transform_base_footprint_to_world.transform.translation.x
                self.odom_transform_msg.transform.translation.y = transform_odom_to_world.transform.translation.y + \
                                                             transform_calculated_to_world.transform.translation.y - \
                                                             transform_base_footprint_to_world.transform.translation.y
                self.odom_transform_msg.transform.translation.z = transform_odom_to_world.transform.translation.z + \
                                                             transform_calculated_to_world.transform.translation.z - \
                                                             transform_base_footprint_to_world.transform.translation.z

                # Find a quaternion q_rot that rotates the existing base_footprint position into the
                # sensor_calculated_base_footprint's position
                q_base = np.array([
                    transform_base_footprint_to_world.transform.rotation.x,
                    transform_base_footprint_to_world.transform.rotation.y,
                    transform_base_footprint_to_world.transform.rotation.z,
                    transform_base_footprint_to_world.transform.rotation.w
                ])
                q_base_inv = np.array([
                    transform_base_footprint_to_world.transform.rotation.x,
                    transform_base_footprint_to_world.transform.rotation.y,
                    transform_base_footprint_to_world.transform.rotation.z,
                    -1 * transform_base_footprint_to_world.transform.rotation.w # Negate for inverse
                ])
                q_calculated = np.array([
                    transform_calculated_to_world.transform.rotation.x,
                    transform_calculated_to_world.transform.rotation.y,
                    transform_calculated_to_world.transform.rotation.z,
                    transform_calculated_to_world.transform.rotation.w
                ])
                q_rot = quaternion_multiply(q_calculated, q_base_inv)
                # Apply rotation q_rot to odom's quaternion
                q_odom = np.array([
                    transform_odom_to_world.transform.rotation.x,
                    transform_odom_to_world.transform.rotation.y,
                    transform_odom_to_world.transform.rotation.z,
                    transform_odom_to_world.transform.rotation.w
                ])
                quaternion = quaternion_multiply(q_rot, q_odom)
                quaternion = quaternion / np.linalg.norm(quaternion)
                self.odom_transform_msg.transform.rotation.x = quaternion[0]
                self.odom_transform_msg.transform.rotation.y = quaternion[1]
                self.odom_transform_msg.transform.rotation.z = quaternion[2]
                self.odom_transform_msg.transform.rotation.w = quaternion[3]

            self.newTag = False

        # Odom>world transform changes when new aruco is seen, but it can be repeated in the
        # meanwhile with last value and new timestamp to avoid exception in coordinate navigator
        self.odom_transform_msg.header.stamp = self.get_clock().now().to_msg()
        #self.odom_transform_broadcaster.sendTransform(self.odom_transform_msg)
        # self.get_logger().info("Odom TF:", self.odom_transform_msg.transform)

        
    def onTag(self, tag_msg):
        """
        Handles incoming tag information messages and resets reference frames.
        @param: self
        @param: tag_msg - information about the tag detected
                          by the vision node
        @result: sets boolean for last tag and makes other
                 tag information globally available

        TODO: I think the position data can be removed from this publisher as it goes through TF broadcaster
            and only ID and floor infomation exchanged through this topic
        """
        #x = tag_msg.pose.position.x
        #y = tag_msg.pose.position.y
        #self.get_logger().info('x =', x)
        #self.get_logger().info('y =', y)
        #self.get_logger().info('ID =', tag_msg.ID)
        self.tag_ID = tag_msg.ID
        #self.tag_dist = tag_msg.distance
        #self.measuredPosition[0] = x
        #self.measuredPosition[1] = y
        self.pose[2] = tag_msg.floor
        #tag_orientation = tag_msg.pose.orientation
        #self.tag_rpy = list(euler_from_quaternion([tag_orientation.x, tag_orientation.y, tag_orientation.z,tag_orientation.w]))
        self.newTag = True


    def onVelCmdEx(self, cmd_vel_msg):
        """
        Does odometry calculations for previous velocity command (that Odrives node repubished after executing the
        command) when new executed velocity command is received.
        Broadcasts TF trnasformation of base_footprint vs odom.

        @param: self
        @param: tag_msg - information about the tag detected
                          by the vision node
        @result: sets boolean for last tag and makes other
                 tag information globally available

        """
        now = time.time()
        td = now - self.time_vel_cmd

        TF_error = False
        try:
            transform_base_to_odom = \
                self.tfBuffer.lookup_transform('odom', 'base_footprint', self.get_clock().now())
        except (tf2_ros.LookupException, tf2_ros.ConnectivityException, tf2_ros.ExtrapolationException) as e:
            TF_error = True
            # TODO figure out how to accumulate the transforms when they can not be applied right away

        if not TF_error:
            # Compute the X and Y distances covered
            dist_x = self.prev_vel_cmd[0] * td # in m
            dist_y = self.prev_vel_cmd[1] * td # in m
            # Compute the starting angle (of tangent of arc)
            orig_angle = 0
            if dist_x == 0:
                if dist_y < 0:
                    orig_angle = -1 * math.pi / 2 # -90 deg in rad
                elif dist_y > 0:
                    orig_angle = math.pi / 2  # 90 deg in rad
            else:
                orig_angle = math.atan(dist_y / dist_x)
            # Compute the Z-angular movement covered
            move_angle = self.prev_vel_cmd[2] * td # in rad
            # Compute the linear movement length (moved arc length) summed from x and y speeds
            dist_travelled = math.sqrt( dist_x**2 + dist_y**2)
            end_x = 0
            end_y = 0
            end_orientation = 0

            if move_angle == 0: # Only linear movement
                if dist_travelled != 0:
                    end_x = dist_x
                    end_y = dist_y
                #self.get_logger().info("Localizer. Only linear.", end_x, end_y)
            elif dist_travelled != 0: # compound movement of linear and rotation forms an arc
                if dist_y == 0:
                    # Simplified version when y movement is not used, to get past a mistake that probably exists
                    # in the full maths in the else part.
                    r = abs(dist_x / move_angle)
                    sign_of_move_angle = move_angle / abs(move_angle)
                    end_orientation = move_angle
                    sign_of_x_speed = dist_x / abs(dist_x)
                    # Move arc's sector is same as move angle
                    end_x = sign_of_x_speed * math.sin(abs(move_angle)) * r
                    end_y = sign_of_move_angle * (r - math.cos(abs(move_angle)) * r)
                    #self.get_logger().info("Localizer. Compound. r, end_x, end_y, end_orientation, ", r, end_x, end_y, end_orientation)
                else:
                    # TODO this has BUG!
                    # Compute the radius of the movement arc
                    r = dist_travelled / move_angle
                    # Compute arc center coordinates (in base_footprint frame at the start of the move)
                    sign_of_move_angle = move_angle/abs(move_angle)
                    center_x = math.sin(orig_angle) * r * sign_of_move_angle * -1
                    center_y = math.cos(orig_angle) * r * sign_of_move_angle
                    # Compute angle of the move arc radius that points to the end of move arc
                    arc_end_perpendicular_angle = orig_angle + move_angle - 90*sign_of_move_angle
                    # Compute coordinates of move end point
                    # TODO probably bug frome here on
                    end_x = center_x + math.cos(arc_end_perpendicular_angle) * r
                    end_y = center_y + math.sin(arc_end_perpendicular_angle) * r
                    # Compute robot orientation at the end of the move (compared to orientation start of move)
                    end_orientation = arc_end_perpendicular_angle + sign_of_move_angle * 90 - orig_angle
                    #self.get_logger().info("Localizer. Compound r, ", r, end_x, end_y, end_orientation)
            else: # Only rotation movement
                end_orientation = move_angle
                #self.get_logger().info("Localizer. only rotation", end_orientation)

            # Compute TF transform of robot base in odom frame
            # Get the Z rotation angle in rad of the base_footprint in odom coordinate frame before the current movement
            # so the new 2D linear coordinates can be calculated from it
            a1, a2, frame_z_rotation = euler_from_quaternion([transform_base_to_odom.transform.rotation.x,
                                                           transform_base_to_odom.transform.rotation.y,
                                                           transform_base_to_odom.transform.rotation.z,
                                                           -1 * transform_base_to_odom.transform.rotation.w])
            # Linear change
            change_x = math.cos(frame_z_rotation) * end_x + math.sin(frame_z_rotation) * end_y
            change_y = math.cos(frame_z_rotation) * end_y - math.sin(frame_z_rotation) * end_x
            #self.get_logger().info("Localizer. Change x and y, end orientation:", change_x, change_y, end_orientation)
            self.base_transform_msg.transform.translation.x = transform_base_to_odom.transform.translation.x + change_x
            self.base_transform_msg.transform.translation.y = transform_base_to_odom.transform.translation.y + change_y
            self.base_transform_msg.transform.translation.z = transform_base_to_odom.transform.translation.z
            # Create quaternion from Z-rotation move
            q_rot = quaternion_from_euler(0, 0, end_orientation)
            # Apply that quaternion to base_footprint's original quaternion
            q_orig = np.array([
                transform_base_to_odom.transform.rotation.x,
                transform_base_to_odom.transform.rotation.y,
                transform_base_to_odom.transform.rotation.z,
                transform_base_to_odom.transform.rotation.w
            ])
            quaternion = quaternion_multiply(q_rot, q_orig)
            quaternion = quaternion / np.linalg.norm(quaternion)
            self.base_transform_msg.transform.rotation.x = quaternion[0]
            self.base_transform_msg.transform.rotation.y = quaternion[1]
            self.base_transform_msg.transform.rotation.z = quaternion[2]
            self.base_transform_msg.transform.rotation.w = quaternion[3]

            self.base_transform_msg.header.stamp = self.get_clock().now().to_msg()
            #self.base_transform_broadcaster.sendTransform(self.base_transform_msg)

            self.prev_vel_cmd[0] = cmd_vel_msg.linear.x
            self.prev_vel_cmd[1] = cmd_vel_msg.linear.y
            self.prev_vel_cmd[2] = cmd_vel_msg.angular.z

            #self.get_logger().info("Time since last vel cmd", td, "prev vel cmd x", self.prev_vel_cmd[0],
            #      "end", end_x, end_y, "change", change_x, change_y)

        self.time_vel_cmd = now



    def onEncoder(self, encoder_msg):
        """
        Handles incoming encoder updates.
        @param: self
        @param encoder_msg - current assumption is that msg
                             contains wheel velocities
        @result: make encoder messages globally available.
                 Possibly process values for odometry
        """
        self.t_wheel = encoder_msg.header.stamp
        self.wheel_speed[0] = encoder_msg.right_front
        self.wheel_speed[1] = encoder_msg.left_front
        self.wheel_speed[2] = encoder_msg.left_back
        self.wheel_speed[3] = encoder_msg.right_back
        self.new_encoder_data = True
    

    def onLine(self,line_msg):
        """
        Handles incoming distances from the line
        @param: self
        @param: line_msg - 2D vector consisting of 
                lateral distance to the line and
                rotation from the line
        @result: make line distances globally available
        """
        self.line_offset[0] = line_msg.vector.y
        self.line_offset[1] = line_msg.vector.z

    def predict(self):
        vx = self.vel_body[0]
        vy = self.vel_body[1]
        w = self.vel_body[2]
        theta = self.pose[5]
        # inverse kinematics of mecanum wheels
        self.vel_body = self.r_wheel/4 * np.dot(self.mec_mat,self.wheel_speed)
        
        # odometry based on velocities from inverse kinematics
        dt = self.encoder_rate
        self.pose[0] += dt * (vx * np.cos(theta) - vy * np.sin(theta))
        self.pose[1] += dt * (vx * np.sin(theta) + vy * np.cos(theta))
        self.pose[5] += w * self.dt

        # Jacobian definition
        self.Jacobian = np.array([[1, 0, self.dt*(-vx*np.sin(theta + dt*(w/2)) - vy*np.cos(theta + dt*(w/2)))], \
                                [0, 1, self.dt*(vx*np.cos(theta + dt*(w/2)) - vy*np.sin(theta + dt*(w/2)))], \
                                [0, 0, 1]])

        self.P = np.dot(self.Jacobian, np.dot(self.P, np.transpose(self.Jacobian))) + self.Q
    

def main(args=None):
    rclpy.init(args=args)
    node = Localizer(10)
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
