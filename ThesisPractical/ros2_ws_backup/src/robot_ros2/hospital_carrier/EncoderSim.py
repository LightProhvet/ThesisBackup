#!/usr/bin/env python

"""
@author: Christian Meurer
@input: Odometry from the simulator
@output: Encoder message with simulated wheel speeds in rad/s based on forward kinematics
         of 4W Mecanum drive robot
"""

import math
import numpy as np
import rclpy
from rclpy.node import Node
from rclpy.parameter import Parameter

from nav_msgs.msg import Odometry, Path
from robot_ros2_msgs.msg import Encoders
from geometry_msgs.msg import PoseStamped, Twist



class EncoderSim(Node):
    def __init__(self, rate):

        super().__init__('EncoderSim')

        # Subscribers
        self.odom_sub = self.create_subscription(Odometry, "/odom", self.onOdom, 10)

        # parameters
        self.declare_parameter("ventral_wheel_distance", Parameter.Type.DOUBLE)
        self.declare_parameter("lateral_wheel_distance", Parameter.Type.DOUBLE)
        self.declare_parameter("wheel_radius", Parameter.Type.DOUBLE)
        self.declare_parameter("encoder_rate", Parameter.Type.DOUBLE)

        self.d_ventral = self.get_parameter("ventral_wheel_distance").value
        self.d_lateral = self.get_parameter("lateral_wheel_distance").value
        self.r_wheel = self.get_parameter("wheel_radius").value
        self.encoder_rate = self.get_parameter("encoder_rate").value

        # Publishers
        self.encoders_pub = self.create_publisher(Encoders, "encoders", 25)
        self.path_pub = self.create_publisher(Path, "groundTruthPath", 1)


        # Messages to be published
        self.encoder_msg = Encoders()
        self.path = Path()

        # define matrix for forward kinematics for Mecanum wheels
        # in following oder: front_right, front_left, back_left, back_right
        self.mec_mat = np.array([[1, 1, self.d_ventral + self.d_lateral],
                                [1, -1, -(self.d_ventral + self.d_lateral)],
                                [1, 1, -(self.d_ventral + self.d_lateral)],
                                [1, -1, self.d_ventral + self.d_lateral]])

        # initialze wheel speed and body velocity variables
        self.wheel_speed = np.zeros(4)
        self.body_vel = np.zeros(3)

        self.rate = self.create_rate(rate)
        self.timer = self.create_timer(0.1, self.run)

    def run(self):
        """
        Main loop of class.
        @param: self
        @result: runs the step function for encoder update
        """
        self.step()
        #self.rate.sleep()


    def step(self):
        """
        Perform an iteration of the EncoderSim loop.
        @param: self
        @result: updates and publishes simulated wheel 
        encoder information (in our case wheel speeds) 
        """
        # publish encoder message
        self.encoder_msg.header.stamp = self.get_clock().now().to_msg()
        self.encoder_msg.right_front = self.wheel_speed[0]
        self.encoder_msg.left_front = self.wheel_speed[1]
        self.encoder_msg.left_back = self.wheel_speed[2]
        self.encoder_msg.right_back = self.wheel_speed[3]
        #self.get_logger().info(str(self.encoder_msg))
        self.encoders_pub.publish(self.encoder_msg)

    def onOdom(self, odom_msg):
        """
        Handles incoming odometry information from simulator.
        @param: self
        @param: odom_msg - robot odometry from simulator
        @result: calculates wheel speeds in rad/s based 
        on forward kinematics of 4W Mecanum wheel drive
        """
        self.body_vel[0] = odom_msg.twist.twist.linear.x
        self.body_vel[1] = odom_msg.twist.twist.linear.y
        self.body_vel[2] = odom_msg.twist.twist.angular.z
        # compute the inverse kinematics
        self.wheel_speed = 1/self.r_wheel * np.dot(self.mec_mat, self.body_vel)
        # self.get_logger().info("wheel_speed: {}".format(self.wheel_speed))


        #Publish ground truth path
        
        self.path.header = odom_msg.header
        poseForPath = PoseStamped()
        poseForPath.header = odom_msg.header
        poseForPath.pose = odom_msg.pose.pose
        self.path.poses.append(poseForPath)
        self.path_pub.publish(self.path)

def main(args=None):
    rclpy.init(args=args)
    node = EncoderSim(10)
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
