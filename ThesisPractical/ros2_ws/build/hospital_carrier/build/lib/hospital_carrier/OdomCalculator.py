#!/usr/bin/env python

'''
Node to calculate and publish odometry from wheel encoders

navigation.ros.org/setup_guides/odom/setup_odom.html
wiki.ros.org/navigation/Tutorials/RobotSetup/Odom/
gist.github.com/atotto/f2754f75bedb6ea56e3e0264ec405dcf

Author: Karl-Erik Kanal
'''

import math
import numpy as np
import rclpy
from rclpy.node import Node

from nav_msgs.msg import Odometry, Path
from geometry_msgs.msg import Point, Pose, Twist, TransformStamped, Vector3, Quaternion
from std_msgs.msg import Float32MultiArray
from tf2_ros import TransformBroadcaster
from tf_transformations import quaternion_from_euler 

class OdomCalculator(Node):
    def __init__(self):

        super().__init__('OdomCalculator')

        # Subscribers
        self.left_wheel_sub = self.create_subscription(Float32MultiArray, "left_wheel_encoder", self.onLeftWheel, 10)
        self.right_wheel_sub = self.create_subscription(Float32MultiArray, "right_wheel_encoder", self.onRightWheel, 10)

        # Publishers
        self.odom_pub = self.create_publisher(Odometry, "/odom", 10)
        self.odom_broadcaster = TransformBroadcaster(self)

        # Messages to be published
        self.odom_msg = Odometry()
        self.transform_msg = TransformStamped()

        self.wheel_separation = 0.37 # Distance between 2 wheels in [m]

        self.x = 0.0
        self.y = 0.0
        self.th = 0.0 # Rotation of the robot. We do this so that the front of the robot is the correct side. Set in radians.
        self.vx = 0.0
        self.vy = 0.0
        self.vth = 0.0

        self.right_wheel_vel_estimate = 0.0
        self.left_wheel_vel_estimate = 0.0
        self.right_wheel_pos_estimate = 0.0
        self.left_wheel_pos_estimate = 0.0 

        self.current_time = self.get_clock().now()
        self.last_time = self.get_clock().now()

        self.create_timer(0.1, self.run)

    def run(self):
        
        # Computing the odometry
        self.current_time = self.get_clock().now()
        current_time_msg = self.get_clock().now().to_msg()

        self.vx = (self.right_wheel_vel_estimate + self.left_wheel_vel_estimate) / 2
        self.vth = (self.right_wheel_vel_estimate - self.left_wheel_vel_estimate) / self.wheel_separation

        dt = (self.current_time.nanoseconds - self.last_time.nanoseconds)
        delta_x = (self.vx * math.cos(self.th) - self.vy * math.sin(self.th)) * dt
        delta_y = (self.vx * math.sin(self.th) + self.vy * math.cos(self.th)) * dt
        delta_th = self.vth * dt

        self.x += delta_x
        self.y += delta_y
        self.th += delta_th

        odom_quat = quaternion_from_euler(0, 0, self.th)

        # Construct odom to base_link transform
        self.transform_msg.header.stamp = current_time_msg
        self.transform_msg.header.frame_id = "odom"
        self.transform_msg.child_frame_id = "base_link"

        self.transform_msg.transform.translation.x = self.x
        self.transform_msg.transform.translation.y = self.y
        self.transform_msg.transform.translation.z = 0.0
        self.transform_msg.transform.rotation.x = odom_quat[0]
        self.transform_msg.transform.rotation.y = odom_quat[1]
        self.transform_msg.transform.rotation.z = odom_quat[2]
        self.transform_msg.transform.rotation.w = odom_quat[3]

        # Publishing the transform
        self.odom_broadcaster.sendTransform(self.transform_msg)

        # Constructing the odometry message
        self.odom_msg.header.frame_id = "odom"
        self.odom_msg.header.stamp = current_time_msg
        self.odom_msg.child_frame_id = "base_link"

        # Set the velocity
        self.odom_msg.twist.twist.linear.x = self.vx
        self.odom_msg.twist.twist.linear.y = self.vy
        self.odom_msg.twist.twist.linear.z = 0.0

        self.odom_msg.twist.twist.angular.x = 0.0
        self.odom_msg.twist.twist.angular.y = 0.0
        self.odom_msg.twist.twist.angular.z = self.vth

        # Set the pose
        self.odom_msg.pose.pose.position.x = self.x
        self.odom_msg.pose.pose.position.y = self.y
        self.odom_msg.pose.pose.position.z = 0.0
        self.odom_msg.pose.pose.orientation.x = odom_quat[0]
        self.odom_msg.pose.pose.orientation.y = odom_quat[1]
        self.odom_msg.pose.pose.orientation.z = odom_quat[2]
        self.odom_msg.pose.pose.orientation.w = odom_quat[3]

        # Publish the message
        self.odom_pub.publish(self.odom_msg)

        self.last_time = self.current_time

    # Callback functions to retrieve encoder data
    def onLeftWheel(self, left_wheel_msg: Float32MultiArray):
        self.left_wheel_pos_estimate = left_wheel_msg.data[0]
        self.left_wheel_vel_estimate = left_wheel_msg.data[1]
    
    def onRightWheel(self, right_wheel_msg: Float32MultiArray):
        self.right_wheel_pos_estimate = right_wheel_msg.data[0]
        self.right_wheel_vel_estimate = right_wheel_msg.data[1]

def main(args=None):
    rclpy.init(args=args)
    node = OdomCalculator()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()