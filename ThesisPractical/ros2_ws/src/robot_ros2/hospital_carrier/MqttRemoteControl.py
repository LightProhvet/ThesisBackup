#!/usr/bin/env python3


import rclpy
from rclpy.node import Node
import time
from std_msgs.msg import String
from geometry_msgs.msg import Twist


class MqttRemoteControl(Node):
    def __init__(self, rate):

        super().__init__('MqttRemoteControl')

        # Subscribers
        self.op_mode_sub = self.create_subscription(String, "op_mode", self.onOpMode, 10)
        self.mqtt_topic_remotecontrol_sub = self.create_subscription(String, "mqtt_remote_control_move", self.onControlMsg, 10)

        # Publishers
        self.body_vel_cmd_pub = self.create_publisher(Twist, "/cmd_vel", 3)
        self.op_mode_request_pub = self.create_publisher(String, "op_mode_change_request", 1)

        # Messages to be published
        self.body_vel_cmd_msg = Twist()

        # Speed settings
        self.rotation_speed = 0.125
        self.linear_speed = 0.125

        self.enabled = False
        self.op_mode_request_msg = String()
        self.command_interval = 0.2 #in sec
        self.command_execution_time_start = 0
        self.cmd_in_execution = ""
        self.cmd_in_buffer = "" #Only one command is held in buffer

        self.rate = self.create_rate(rate)
        self.timer = self.create_timer(0.1, self.run)



    def run(self):
        self.step()
        #self.rate.sleep()



    def step(self):

        if self.cmd_in_execution == "" and self.cmd_in_buffer != "":
            self.cmd_in_execution = self.cmd_in_buffer
            self.cmd_in_buffer = ""

        if self.cmd_in_execution != "":
            if self.command_execution_time_start == 0: #fresh first command
                self.command_execution_time_start = time.time()
            elif time.time() > self.command_execution_time_start + self.command_interval: #time to finish this one
                self.cmd_in_execution = self.cmd_in_buffer
                self.cmd_in_buffer = ""
                if self.cmd_in_execution != "": #if next command was found in buffer
                    self.command_execution_time_start = time.time()
                else: #no next command was found in buffer
                    self.command_execution_time_start = 0

        self.body_vel_cmd_msg.linear.x = 0.0
        self.body_vel_cmd_msg.linear.y = 0.0
        self.body_vel_cmd_msg.angular.z = 0.0

        if self.cmd_in_execution == "rotate-right":
            self.body_vel_cmd_msg.angular.z = -1*self.rotation_speed
        elif self.cmd_in_execution == "rotate-left":
            self.body_vel_cmd_msg.angular.z = self.rotation_speed
        elif self.cmd_in_execution == "right":
            self.body_vel_cmd_msg.linear.y = -1*self.linear_speed
        elif self.cmd_in_execution == "left":
            self.body_vel_cmd_msg.linear.y = self.linear_speed
        elif self.cmd_in_execution == "up":
            self.body_vel_cmd_msg.linear.x = self.linear_speed
        elif self.cmd_in_execution == "down":
            self.body_vel_cmd_msg.linear.x = -1*self.linear_speed

        if self.enabled:
            self.body_vel_cmd_pub.publish(self.body_vel_cmd_msg)

    def onOpMode(self, op_mode_msg):
        self.enabled = op_mode_msg.data == "mqtt"

    def onControlMsg(self, control_msg):
        if not self.enabled:
            # When user starts to use the controls in the middle of other action or when paused
            # lets ask to change the operation mode.
            self.op_mode_request_msg = "mqtt_control_enable"
            self.op_mode_request_pub.publish(self.op_mode_request_msg)

        self.cmd_in_buffer = control_msg.data
        self.get_logger().info("REMOTE COMMAND:" + str(control_msg.data))


def main(args=None):
    rclpy.init(args=args)
    node = MqttRemoteControl(10)
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()