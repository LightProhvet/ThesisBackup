#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from rclpy.parameter import Parameter
import paho.mqtt.client as mqtt
import tf2_ros
from std_msgs.msg import String
from robot_ros2_msgs.msg import Tag


class MqttOdomAndStatus(Node):
    def __init__(self, keepalive):
        super().__init__('MqttOdom')

        #Parameters
        self.declare_parameter('host', Parameter.Type.STRING)
        self.declare_parameter('port', Parameter.Type.INTEGER)
        self.declare_parameter('username', Parameter.Type.STRING)
        self.declare_parameter('password', Parameter.Type.STRING)
        self.declare_parameter('odom_topic', Parameter.Type.STRING)
        self.declare_parameter('ready_topic', Parameter.Type.STRING)
        self.declare_parameter('start_topic', Parameter.Type.STRING)
        self.declare_parameter('finish_topic', Parameter.Type.STRING)
        self.declare_parameter('ca_file', Parameter.Type.STRING)
        
        self.host = self.get_parameter('host').value
        self.port = self.get_parameter('port').value
        self.username = self.get_parameter('username').value
        self.password = self.get_parameter('password').value
        self.odom_topic = self.get_parameter('odom_topic').value
        self.ready_topic = self.get_parameter('ready_topic').value
        self.start_topic = self.get_parameter('start_topic').value
        self.finish_topic = self.get_parameter('finish_topic').value
        self.ca_file = self.get_parameter('ca_file').value

        self.keepalive = keepalive
        self.client = mqtt.Client()
        self.client.username_pw_set(username=self.username, password=self.password)
        self.client.tls_set(ca_certs=self.ca_file)
        self.client.tls_insecure_set(True)

        # Transform listener
        self.tfBuffer = tf2_ros.Buffer()
        self.listener = tf2_ros.TransformListener(self.tfBuffer, self)

        # Subscriber to get floor - right now only thing that knows floor is the aruco detector, change in future
        self.tag_sub = self.create_subscription(Tag, "arucoTag", self.onTag, 10)

        self.odrive_status_sub = self.create_subscription(String, "odrive_status", self.onOdriveStatus, 10)
        self.route_started_sub = self.create_subscription(String, "route_started", self.onRouteStarted, 10)
        self.route_finished_sub = self.create_subscription(String, "route_finished", self.onRouteFinished, 10)

        self.floor = 0

        self.rate = self.create_rate(10)
        self.timer = self.create_timer(0.1, self.run)

        if not rclpy.ok():
            self.client.disconnect()
            self.client.loop_stop()

    def onTag(self, tag_msg):
        self.floor = tag_msg.floor

    def onOdriveStatus(self, msg):
        if msg.data == "ready":
            self.client.publish(self.ready_topic, "rc-ready")

    def onRouteStarted(self, msg):
        if msg.data.find('-'):
            location_name = msg.data[:msg.data.find('-')]
            self.client.publish(self.start_topic, location_name)
        else:
            self.client.publish(self.start_topic, msg.data)

    def onRouteFinished(self, msg):
        if msg.data.find('-'):
            location_name = msg.data[(msg.data.find('-')+1):]
            self.client.publish(self.finish_topic, location_name)
        else:
            self.client.publish(self.finish_topic, msg.data)

    def run(self):
        self.client.connect_async(self.host, self.port, self.keepalive)
        self.client.loop_start()
        self.step()
        #self.rate.sleep()

    def step(self):
        error = False
        try:
            transform = self.tfBuffer.lookup_transform('map', 'base_footprint', self.get_clock().now())
        except (tf2_ros.LookupException, tf2_ros.ConnectivityException, tf2_ros.ExtrapolationException) as e:
            error = True

        if not error:
            location_str = "time:" + str(transform.header.stamp.secs)
            location_str = location_str + ",x:" + str(transform.transform.translation.x)
            location_str = location_str + ",y:" + str(transform.transform.translation.y)
            location_str = location_str + ",floor:" + str(self.floor) + "\n"

            self.client.publish(self.odom_topic, location_str)

def main(args=None):
        rclpy.init(args=args)
        node = MqttOdomAndStatus(
            keepalive=60
        )
        rclpy.spin(node)
        rclpy.shutdown()

if __name__ == '__main__':
    main()
