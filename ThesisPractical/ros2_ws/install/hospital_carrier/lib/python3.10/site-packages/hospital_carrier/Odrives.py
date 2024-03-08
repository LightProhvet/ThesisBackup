#!/usr/bin/env python3

#TODO: Should we make a message type with header for Odrive errors?
#TODO: Detect if odrive error condition has passed and publish "OK" again.
#TODO: Is it better to have stop_motors and start_motors as service or subscriber?


import rclpy
from rclpy.node import Node
from rclpy.parameter import Parameter

from std_msgs.msg import String, Float32, Bool, Float32MultiArray
from geometry_msgs.msg import Twist
import numpy as np


import signal
import time
import usb.core
import fibre.protocol
import serial
import math
from .odrive_axes_of import enable_only_axes, is_odrv_enabled
from .odrives_connect import connect_odrives, odrive_ids
from .odrives_config import config_odrives
from .odrives_calibrate import calibrate_odrives
from .odrive_errors import check_odrive_errors, ODriveAxisError, ODriveVoltageTooLow, ODriveUARTError, clear_odrive_errors
from .watchdog import start_watchdogs

import odrive.enums
from .odrive_axes_of import axes_of, is_axis_enabled_iter


class Odrives(Node):
    def __init__(self):
        super().__init__('Odrives')
        # Subscribers
        self.cmd_vel_sub = self.create_subscription(Twist, "/cmd_vel", self.onVelCmd, 10)
        self.motor_cmd_sub = self.create_subscription(Bool, "motor_cmd", self.onMotorCmd, 10)

        # Publishers
        self.odrive_status_pub = self.create_publisher(String, "odrive_status", 1)
        self.battery_voltage_pub = self.create_publisher(Float32, "battery_voltage", 1)
        self.odrive_errors_pub = self.create_publisher(String, "odrive_errors", 10)
        self.op_mode_change_req_pub = self.create_publisher(String, "op_mode_change_request", 1)
        self.cmd_vel_executed_pub = self.create_publisher(Twist, "cmd_vel_executed", 10)
        self.left_wheel_pub = self.create_publisher(Float32MultiArray, "left_wheel_encoder", 10)
        self.right_wheel_pub = self.create_publisher(Float32MultiArray, "right_wheel_encoder", 10)

        # Messages to be published
        self.odrive_status_msg = String()
        self.battery_voltage_msg = Float32()
        self.odrive_errors_msg = String()

        self.left_wheel_msg = Float32MultiArray()
        self.right_wheel_msg = Float32MultiArray()

        # parameters

        self.declare_parameters(namespace= '', parameters=[
            ("ventral_wheel_distance", Parameter.Type.DOUBLE),
            ("lateral_wheel_distance", Parameter.Type.DOUBLE),
            ("wheel_radius", Parameter.Type.DOUBLE),
            ("encoder_resolution", Parameter.Type.INTEGER)
        ])

        self.d_ventral = self.get_parameter("ventral_wheel_distance").value
        self.d_lateral = self.get_parameter("lateral_wheel_distance").value
        self.r_wheel = self.get_parameter("wheel_radius").value
        self.encoder_resolution = self.get_parameter("encoder_resolution").value
        

        # self.v_needed = rospy.get_param("odrive_params/voltage_needed", 34.0)
        self.battery_voltage_publish_interval = 60  # seconds

        self.odrv = None
        self.is_cmd = False
        self.cmd_msg = None
        self.body_vel = np.zeros(3)
        self.wheel_speed = np.zeros(4)
        self.battery_voltage = 0
        self.battery_voltage_last_publish_time = time.time()

        # define matrix for forward kinematics for Mecanum wheels
        # in following oder: rear_left, front_left, front_right, back_right
        # Order comes from odrives connections order, marks come from encoder 
        # wires connections that are identical for all wheels.
        self.mec_mat = np.array([[ 1,  1, -(self.d_ventral + self.d_lateral)],
                                 [ 1, -1, -(self.d_ventral + self.d_lateral)],
                                 [-1, -1, -(self.d_ventral + self.d_lateral)],
                                 [-1,  1, -(self.d_ventral + self.d_lateral)]])

        self.rate = self.create_rate(10) #TODO what frequency?
        
        if not rclpy.ok():
            self.get_logger().info("Cleaning up..")
            self.clean_shutdown()

        self.odrive_status_msg.data = "connecting"
        self.odrive_errors_msg.data = "OK"
        self.odrive_status_pub.publish(self.odrive_status_msg)
        self.odrive_errors_pub.publish(self.odrive_errors_msg)

        connection_success = False

        # get number of active odrives to check later that they are successfully connected
        odrvs_count = 0
        for id in odrive_ids:
            if is_odrv_enabled(id):
                odrvs_count += 1

        while not connection_success:
            try:
                # this is a list of OdriveConnection objects where .odrv property
                # of each list item is an instance of ODriveUART
                odrv = connect_odrives()

            except (usb.core.USBError, fibre.protocol.ChannelBrokenException) as e:
                self.get_logger().info('USB error {} ({})'.format(type(e).__name__, e))
                self.odrive_errors_msg.data = e
                self.odrive_errors_pub.publish(self.odrive_errors_msg)

            except (ODriveUARTError, serial.SerialException) as e:
                self.get_logger().info('UART error {} ({})'.format(type(e).__name__, e))
                self.odrive_errors_msg.data = e
                self.odrive_errors_pub.publish(self.odrive_errors_msg)

            except ODriveVoltageTooLow:
                self.odrive_errors_msg.data = "Error: Odrive voltage too low!"
                self.odrive_errors_pub.publish(self.odrive_errors_msg)
                self.publish_battery_voltage()
                self.op_mode_change_req_pub.publish("disable")

            if len(odrv) == odrvs_count:
                connection_success = True
                self.odrv = odrv
                self.publish_battery_voltage()
                start_watchdogs(self.odrv)
            else:
                self.get_logger().info("{} odrives of {} connected. Retrying in 2 seconds.".format(len(odrv), odrvs_count))
                time.sleep(2)

        self.odrive_status_msg.data = "calibrating"
        self.odrive_status_pub.publish(self.odrive_status_msg)

        calibration_success = False

        while not calibration_success:
            try:
                clear_odrive_errors(self.odrv)
                config_odrives(self.odrv)
                #clear_odrive_errors(self.odrv)
                calibrate_odrives(self.odrv)
                check_odrive_errors(self.odrv)

                calibration_success = True

            except ODriveAxisError:
                self.stop_motors()

                wait = 1  # seconds
                self.get_logger().info('Waiting {} seconds before restarting...'.format(wait))
                time.sleep(wait)

            except RestartException:
                pass

        time.sleep(0.2)
        self.start_motors()
        self.odrive_status_msg.data = "ready"
        self.odrive_status_pub.publish(self.odrive_status_msg)
        self.timer = self.create_timer(0.1, self.run)

    def start_motors(self):
        self.get_logger().info('Starting motor control...')
        for axis in axes_of(self.odrv):
            with axis.lock:
                axis.axis.controller.input_vel= 0
                axis.axis.requested_state = odrive.enums.AXIS_STATE_CLOSED_LOOP_CONTROL
                time.sleep(0.2)
                self.get_logger().info("Odrive axis state " + str(axis.axis.current_state))

    def stop_motors(self):
        self.body_vel = np.zeros(3)
        self.wheel_speed = np.zeros(4)
        self.get_logger().info('Stopping all axes...')
        for axis in axes_of(self.odrv):
            with axis.lock:
                axis.axis.requested_state = odrive.enums.AXIS_STATE_IDLE
        self.get_logger().info('Done stopping all axes.')

    def wheel_velocities_from_cmd(self, cmd_msg):
        # compute the inverse kinematics
        self.body_vel[0] = cmd_msg.linear.x
        self.body_vel[1] = cmd_msg.linear.y
        self.body_vel[2] = cmd_msg.angular.z
        self.wheel_speed = 5 / (2*math.pi*self.r_wheel) * np.dot(self.mec_mat, self.body_vel)

        # turns/s,  15:1 is the gearing from motor axle where the encoder sits to wheels
        #self.get_logger().info("wheel_speed: {}".format(self.wheel_speed))
        self.get_logger().info("body vel " + str(self.body_vel))
        #self.get_logger().info("wheel speeds", self.wheel_speed)

    def set_motor_velocities(self):
        axis_filter = is_axis_enabled_iter(self.odrv)
        for axis, wheelSpeed in zip(axes_of(self.odrv), filter(lambda _: next(axis_filter), self.wheel_speed)):

            # TODO add try-except and if PortNotOpen error then
            #         self.op_mode_change_req_pub.publish("disable")
            #         self.odrive_errors_msg.data = e
            #         self.odrive_errors_pub.publish(self.odrive_errors_msg)

            with axis.lock:
                axis.axis.controller.input_vel = wheelSpeed  # turns per second
            check_odrive_errors(self.odrv)

    def publish_battery_voltage(self):
        if len(self.odrv) == 0:
            self.battery_voltage = 0
        else:
            o = self.odrv[0]
            with o.lock:
                try:
                    self.battery_voltage = o.odrv.vbus_voltage
                except ODriveUARTError: # ('No response') TODO
                    raise
        self.battery_voltage_msg.data = self.battery_voltage
        self.battery_voltage_pub.publish(self.battery_voltage_msg)
        self.battery_voltage_last_publish_time = time.time()

    def clean_shutdown(self):
        
        self.stop_motors()
        
        if self.odrv is not None:
            for odrv in self.odrv:
                try:
                    odrv.stop_conn()
                except:
                    self.get_logger().info("Odrive node shutdown process: Exception in disconnecting from Odrives.")
                    raise

    def onMotorCmd(self, motor_cmd_msg):   # TODO make a service instead
        if motor_cmd_msg.data:
            self.start_motors()
        else:
            self.stop_motors()

    def onVelCmd(self, cmd_vel_msg):
        self.cmd_msg = cmd_vel_msg
        self.is_cmd = True

    def sendEncoderPositionAndRotation(self):
        i = 0
        for axis in axes_of(self.odrv):
            with axis.lock:
                position = axis.axis.encoder.pos_estimate
                velocity = axis.axis.encoder.vel_estimate

                #self.get_logger().info(str(position))
                #self.get_logger().info(str(rotation))
                #self.get_logger().info(str(i)+ " ratas")

                # Front-left and Front-Right wheel
                if i == 1 or i == 2:
                    info_arr = [position, velocity]

                    if i == 1:
                        self.left_wheel_msg.data = info_arr
                        self.left_wheel_pub.publish(self.left_wheel_msg)

                    elif i == 2:
                        self.right_wheel_msg.data = info_arr
                        self.right_wheel_pub.publish(self.right_wheel_msg)

                i+=1


    def run(self):

        start = time.time()  #TODO remove after test
        if self.is_cmd:
            self.step()

        now = time.time()
        #self.get_logger().info("Odives step took", now - start, "s to run.")  #TODO remove after test
        if now - self.battery_voltage_last_publish_time >= self.battery_voltage_publish_interval:
            self.publish_battery_voltage()
            self.get_logger().info('Battery voltage (at first ODrive): {:.03f} V'.format(self.battery_voltage))

        

    def step(self):

        if self.is_cmd:
            cmd_msg = self.cmd_msg
            self.wheel_velocities_from_cmd(cmd_msg)
            self.set_motor_velocities()
            self.cmd_vel_executed_pub.publish(cmd_msg)
            self.is_cmd = False
            self.sendEncoderPositionAndRotation()

class RestartException(Exception):
    pass



def main(args=None):
    rclpy.init(args=args)
    node = Odrives()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
        main()

