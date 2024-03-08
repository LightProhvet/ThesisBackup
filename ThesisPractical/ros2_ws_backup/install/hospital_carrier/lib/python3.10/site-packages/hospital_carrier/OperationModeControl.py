#!/usr/bin/env python3

"""
OperationModeControl node subscribes to topics that show the status of the system
and it publishes to topic "op_mode" that will determine if the robot is allowed to move at all
and what other node should be controlling the movement.
Op_mode message value can be:
    paused      - means the system is okay and waiting for new command
    paused_en_route - waiting the door or elevator to open
    disabled    - means there is a problem like Odrive not connecting or battery dangerously low etc that prevents
                  safe operation
    follower    - moving by line on route to set destination, passing obstacles
    coordinate_navigator  - move to prescribed coordinate by means of odometry, for example before and in the elevator
    (location_discovery - NOT IMPLEMENTED YET robot that has been unpowered does some looking around to detect it's
                            exact location)
    ps4controller - control by Playstation remote
    (mqtt        - NOT IMPLEMENTED YET: command from UI always forwarded)

Op_mode is changed when:
    - paused robot receives a new destination command from server: paused -> follower. Requested by RouteControl node.
    - in follower mode an aruco tag is seen that is last one either in the end of route or before elevator or door:
        follower -> coordinate_navigator. Requested by RouteControl node.
    - coordinate_navigator node announces that the coordinate has been reached. Next mode can be either:
        paused_en_route, paused, coordinate_navigator or follower. Requested by RouteControl node.
    - PS4Controller node sends a click or doubleclick of it's button - switches back and forth between ps4controller
        mode and previously active mode.
    - When battery runs low or Odrive has a problem everything else is overridden and mode becomes disabled.


Nodes that can publish to "/cmd_vel" a.k.a "body_vel_cmd" topic should only do that when "op_mode"
message matches their name.
"""

import rclpy
from rclpy.node import Node
from rclpy.parameter import Parameter

from std_msgs.msg import String, Float32
from geometry_msgs.msg import Twist


class OperationModeControl(Node):

    def __init__(self):
        super().__init__('OperationModeControl')
        # Subscribers
        self.modechange_req_sub = self.create_subscription(String, "op_mode_change_request", self.onChangeReq, 10)
        self.battery_voltage_sub = self.create_subscription(Float32, "battery_voltage", self.onBatteryVolt, 10)
        self.odrive_status_sub = self.create_subscription(String, "odrive_status", self.onOdriveStatus, 10)
        self.odrive_errors_sub = self.create_subscription(String, "odrive_errors", self.onOdriveError, 10)
        # aruco read
        # route - last tag

        # Publishers
        self.op_mode_pub = self.create_publisher(String, "op_mode", 10)
        self.body_vel_cmd_pub = self.create_publisher(Twist, "/cmd_vel", 25)

        # Messages to be published
        self.op_mode_msg = String()
        self.body_vel_cmd_msg = Twist()

        self.op_mode_msg.data = "paused"   # "follower" "coordinate_navigator" "paused_en_route" "disabled" "paused" "mqtt" "ps4controller"
        self.prev_op_mode_msg_str = self.op_mode_msg.data
        self.temp_prev_op_mode_msg_str = self.op_mode_msg.data
        
        self.declare_parameter('simulation', Parameter.Type.BOOL)
        self.declare_parameter('test_without_driving', Parameter.Type.BOOL)
        self.declare_parameter('voltage_needed', Parameter.Type.DOUBLE)

        self.is_sim = self.get_parameter('simulation').value
        self.is_test = self.get_parameter('test_without_driving').value

        self.new_request = None
        self.odrivesOK = False
        self.odriveError = False
        self.batteryVolt = 40
        self.v_needed = self.get_parameter("voltage_needed").value

        self.timer = self.create_timer(0.1, self.run)

    def onChangeReq(self, change_req_msg):
        self.get_logger().info("change_req_msg " + change_req_msg.data)
        self.new_request = change_req_msg.data

    def onBatteryVolt(self, battery_volt_msg):
        self.batteryVolt = battery_volt_msg.data

    def onOdriveStatus(self, odrive_status_msg):
        self.odrivesOK = odrive_status_msg.data == "ready"

    def onOdriveError(self, odrive_error_msg):
        if odrive_error_msg.data != "OK":
            self.odriveError = True
        else:
            self.odriveError = False

    def run(self):

        self.op_mode_pub.publish(self.op_mode_msg)
        self.step()

    def step(self):
        if self.new_request is not None:
            self.prev_op_mode_msg_str = self.temp_prev_op_mode_msg_str
            self.temp_prev_op_mode_msg_str = self.op_mode_msg.data
            if not (self.is_sim or self.is_test) and (not self.odrivesOK or self.odriveError):   #Respect Odrive issues when not in simulation.
                self.op_mode_msg.data = "disabled"
            elif self.batteryVolt < self.v_needed:
                self.op_mode_msg.data = "disabled"
            else:
                if self.new_request == "ps4controller-click":
                    self.get_logger().info("ps4controller-click")
                    if self.op_mode_msg.data == "paused" and self.prev_op_mode_msg_str == "ps4controller":
                        self.op_mode_msg.data = "ps4controller"
                    elif self.op_mode_msg.data == "paused" and self.prev_op_mode_msg_str == "follower":
                        self.op_mode_msg.data = "follower"
                    else:
                        self.op_mode_msg.data = "paused"

                elif self.new_request == "ps4controller-doubleclick":
                    self.get_logger().info("ps4controller-doubleclick")
                    if self.op_mode_msg.data == "paused" and self.prev_op_mode_msg_str == "follower":
                        self.op_mode_msg.data = "ps4controller"
                    elif self.op_mode_msg.data == "paused" and self.prev_op_mode_msg_str == "ps4controller":
                        self.op_mode_msg.data = "follower"
                    elif self.op_mode_msg.data == "paused":
                        self.op_mode_msg.data = "ps4controller"
                    elif self.op_mode_msg.data == "ps4controller":
                        self.op_mode_msg.data = "follower"
                    elif self.op_mode_msg.data == "follower":
                        self.op_mode_msg.data = "ps4controller"

                elif self.new_request == "start_coordinate_nav":
                    self.op_mode_msg.data = "coordinate_navigator"

                elif self.new_request == "start_follower":
                    self.op_mode_msg.data = "follower"

                elif self.new_request == "start_paused_en_route":
                    self.op_mode_msg.data = "paused_en_route"

                elif self.new_request == "start_paused":
                    # self.get_logger().info("request start_paused")
                    self.op_mode_msg.data = "paused"

                elif self.new_request == "mqtt_control_enable":
                    self.op_mode_msg.data = "mqtt"

                elif self.new_request == "mqtt_control_disable": # not implemented anywhere yet
                    # self.get_logger().info("request mqtt_control_disable")
                    self.op_mode_msg.data = "paused"

                elif self.new_request == "disable":
                    self.op_mode_msg.data = "disabled"


            self.op_mode_pub.publish(self.op_mode_msg)
            
            if self.prev_op_mode_msg_str != self.op_mode_msg.data:
                self.get_logger().info("NEW OPERATION MODE: " + str(self.op_mode_msg.data))
            # Publishes vel_cmd zeros to stop robot when status changes
            self.body_vel_cmd_msg.linear.x = 0.0
            self.body_vel_cmd_msg.linear.y = 0.0
            self.body_vel_cmd_msg.angular.z = 0.0
            self.body_vel_cmd_pub.publish(self.body_vel_cmd_msg)
            self.new_request = None

        # If opmode was disabled but odrive problems have now got resolved, go to paused mode
        elif self.op_mode_msg.data == "disabled" and self.odrivesOK and not self.odriveError:
            self.op_mode_msg.data = "paused"
            self.op_mode_pub.publish(self.op_mode_msg)
            self.get_logger().info("NEW OPERATION MODE: " + str(self.op_mode_msg.data)) 

        # Repeat motors stop command if mode does not allow to move, if first time was missed
        if self.op_mode_msg.data in ["disabled", "paused", "paused_en_route"]:
            self.body_vel_cmd_msg.linear.x = 0.0
            self.body_vel_cmd_msg.linear.y = 0.0
            self.body_vel_cmd_msg.angular.z = 0.0
            self.body_vel_cmd_pub.publish(self.body_vel_cmd_msg)

def main(args=None):
        rclpy.init(args=args)
        node = OperationModeControl()
        rclpy.spin(node)
        rclpy.shutdown()

if __name__ == '__main__':
    main()
