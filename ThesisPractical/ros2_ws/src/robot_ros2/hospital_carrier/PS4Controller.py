#!/usr/bin/env python3

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'lib'))

import rclpy
from rclpy.node import Node
from rclpy.parameter import Parameter

from std_msgs.msg import Int16, String, Bool, Float32
from geometry_msgs.msg import Twist

import approxeng.input.controllers as ai_controllers
import approxeng.input.selectbinder as ai_selectbinder
import approxeng.input.dualshock4 as ai_dualshock4

import signal
import time


class RestartException(Exception):
    pass

class PS4Controller(Node):

    def __init__(self):

        super().__init__('PS4Controller')

        # Subscribers
        self.op_mode_sub = self.create_subscription(String, "op_mode", self.onOpMode, 10)
        self.battery_voltage_sub = self.create_subscription(Float32, "battery_voltage", self.onBatteryVolt, 10)

        # Publishers
        self.body_vel_cmd_pub = self.create_publisher(Twist, "/cmd_vel", 25)
        self.motor_cmd_pub = self.create_publisher(Bool, "motor_cmd", 25)
        self.op_mode_request_pub = self.create_publisher(String, "op_mode_change_request", 3)

        # Messages to be published
        self.body_vel_cmd_msg = Twist()
        self.motor_cmd_msg = Bool()
        self.op_mode_request_msg = String()

        self.declare_parameter("vel_x_const_remote_control", Parameter.Type.DOUBLE)
        self.declare_parameter("voltage_warning", Parameter.Type.DOUBLE)

        self.vel_x_const_remote_control = self.get_parameter("vel_x_const_remote_control").value
        self.voltage_warning = self.get_parameter("voltage_warning").value

        self.controller = None
        self.enabled = False
        self.waiting_for_controller_reconnect = False
        self.controller_unbind_fn = lambda: None
        
        self.button_press_time = time.time()
        self.double_press_interval = 2

        self.timer = self.create_timer(0.1, self.step)
        

    def onOpMode(self, op_mode_msg):
        self.enabled = op_mode_msg.data == "ps4controller"

    def onBatteryVolt(self, battery_volt_msg):
        if battery_volt_msg.data < self.voltage_warning:
            if self.controller.connected:
                try:
                    self.controller.set_leds(1, 1, 1)  # HSV; red
                except IOError:
                    pass

    def connect_ps4_controller(self):
        requirements = ai_controllers.ControllerRequirement(require_class=ai_dualshock4.DualShock4)
        discoveries = ai_controllers.find_matching_controllers(requirements)
        self.controller_unbind_fn = ai_selectbinder.bind_controllers(*discoveries)
        return discoveries[0].controller

    def has_ps_button_been_pressed(self):
        self.controller.check_presses()
        # presses property contains presses between last 2 calls to check_presses()
        presses = self.controller.presses
        #if presses.has_presses:
            #self.get_logger().info(str(presses))
        return 'home' in presses

    def joysticks_to_vel_cmd(self, lx, ly, rx):
        # lx and ly determine translation, rx determines pure rotation.
        return [self.vel_x_const_remote_control * ly, self.vel_x_const_remote_control * -lx, self.vel_x_const_remote_control * -rx]

        # Old version:
        # For the theory, see https://web.archive.org/web/20181228164431/https://www.chiefdelphi.com/media/papers/download/2614
        '''scale = 100000   # lx, ly, rx are in scale of -1...1
        v_front_left = ly + lx + rx  # 50 000 easily... max 300 000
        v_front_right = -1 * (ly - lx - rx)
        v_rear_left = ly - lx + rx
        v_rear_right = -1 * (ly + lx - rx)'''

    def request_motors_start(self):
        self.motor_cmd_msg.data = True
        self.motor_cmd_pub.publish(self.motor_cmd_msg)
        
    def request_motors_stop(self):
        self.motor_cmd_msg.data = False
        self.motor_cmd_pub.publish(self.motor_cmd_msg)

    def manage_ps4_connection(self):
        if self.controller is not None and self.controller.connected:
            return
        
        try:
            if not self.waiting_for_controller_reconnect:
                self.get_logger().info('Connecting to a PS4 controller...')
                
            ps4_controller = self.connect_ps4_controller()
            self.waiting_for_controller_reconnect = False
                
            # self.request_motors_start()

            ps4_controller.axes.set_axis_centres()

            ps4_controller.set_leds(0.6, 1, 0.1)  # HSV; pale blue
            self.get_logger().info('PS4 controller is now connected.')
            self.get_logger().info('Press "PS" button on controller to pause and unpause. Double press to switch between PS4 remote and follower.')
    
            self.controller = ps4_controller

        except IOError as e:
            if not self.waiting_for_controller_reconnect:  # Print log only if it is news
                self.get_logger().info('PS4 controller not connected ({})'.format(e))
    
                self.request_motors_stop()
    
                wait = 0.5  # seconds
                self.get_logger().info('Waiting {} seconds before reconnecting...'.format(wait))
                time.sleep(wait)
    
                self.waiting_for_controller_reconnect = True

        except RestartException:
            raise

    def step(self):
        
        self.manage_ps4_connection()
        # If operation mode is PS4controller, get joysticks position 
        # and publish velocity command
        if self.enabled:
            lx, ly, rx = self.controller['lx', 'ly', 'rx']
            # self.get_logger().info(lx, ly, rx)
            vel_x, vel_y, vel_az = self.joysticks_to_vel_cmd(lx, ly, rx)
            # self.get_logger().info(vel_x, vel_y, vel_az)
            self.body_vel_cmd_msg.linear.x = vel_x
            self.body_vel_cmd_msg.linear.y = vel_y
            self.body_vel_cmd_msg.angular.z = vel_az
            #self.get_logger().info("Publishitav sõnum " + str(self.body_vel_cmd_msg))
            self.body_vel_cmd_pub.publish(self.body_vel_cmd_msg)

        # Watch for PS button presses to change operation mode.
        if self.has_ps_button_been_pressed():
            now = time.time()
            if now - self.button_press_time <= self.double_press_interval:
                self.op_mode_request_msg.data = "ps4controller-doubleclick"
            else:
                self.op_mode_request_msg.data = "ps4controller-click"
                self.button_press_time = time.time()
                
            self.op_mode_request_pub.publish(self.op_mode_request_msg)
            time.sleep(0.25) # just for debouncing button
            
        # On odrive finding the battery voltage too low, make the LED of the controller red
        '''if :
            try:
                with connect_ps4_controller() as ps4_controller:
                    ps4_controller.set_leds(1, 1, 1)  # HSV; red
            except IOError:
                pass'''
        
        
    def cleanup(self):
        self.controller_unbind_fn()
    
def main(args=None):
    rclpy.init(args=args)
    try:
        node = PS4Controller()
        rclpy.spin(node)
    finally:
        node.cleanup()
        
    rclpy.shutdown()


if __name__ == '__main__':
    main()
