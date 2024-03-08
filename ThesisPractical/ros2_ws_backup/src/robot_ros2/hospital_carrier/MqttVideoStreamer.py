#!/usr/bin/env python3

"""
@author: Maksim Maksimov
"""

import rclpy
from rclpy.node import Node
from rclpy.parameter import Parameter
import cv2
import paho.mqtt.client as mqtt
import cv_bridge
import base64
import numpy as np
from sensor_msgs.msg import Image
from functools import partial
import time

class MqttVideoStreamer(Node):
    def __init__(self, keepalive):
        super().__init__('MqttVideoStreamer')

        #Parameters
        self.declare_parameter('host', Parameter.Type.STRING)
        self.declare_parameter('port', Parameter.Type.INTEGER)
        self.declare_parameter('username', Parameter.Type.STRING)
        self.declare_parameter('password', Parameter.Type.STRING)
        self.declare_parameter('produce_topic', Parameter.Type.STRING)
        self.declare_parameter('ca_file', Parameter.Type.STRING)


        self.host = self.get_parameter('host').value
        self.port = self.get_parameter('port').value
        self.username = self.get_parameter('username').value
        self.password = self.get_parameter('password').value
        self.produce_topic = self.get_parameter('produce_topic').value
        self.ca_file = self.get_parameter('ca_file').value

        self.keepalive = keepalive
        self.client = mqtt.Client()
        self.client.username_pw_set(username=self.username, password=self.password)
        self.client.tls_set(ca_certs=self.ca_file)
        self.client.tls_insecure_set(True)
        self.client.on_connect = self.on_connect
        self.topics_dict = {
            "/hospital_carrier/camera_stream2": "/robot/aatest/stream/camera2",
            "/camera/color/image_raw": "/robot/aatest/stream/camera1"
        }
        self.subscribers = []
        self.timer = self.create_timer(0.1, self.run)

        if not rclpy.ok():
            # unregister ROS subscribers
            for subscriber in self.subscribers:
                self.destroy_subscription(subscriber)

            self.client.disconnect()
            self.client.loop_stop() #TODO this seems to hang intermittently
            self.get_logger().info("Videostreamer loop stopped successfully")

            self.client.loop_stop()
        

    def run(self):
        # ROS topic -> MQTT topic
        for ros_topic, mqtt_topic in self.topics_dict.items():
            subscriber = self.create_subscription(Image, ros_topic, partial(self.on_image, mqtt_topic), 10)
            #self.get_logger().info("Subscribed to " + str(ros_topic))
            self.subscribers.append(subscriber)
        self.client.connect_async(self.host, self.port, self.keepalive)
        self.client.loop_start()

    def on_connect(self, client, userdata, flags, rc):
        self.get_logger().info("MqttVideoStreamer node mqtt connected with result code "+str(rc))

    def on_image(self, mqtt_topic, image_msg):
        img = cv_bridge.CvBridge().imgmsg_to_cv2(image_msg, desired_encoding='bgr8')
        success, content = cv2.imencode('.png', img, [cv2.IMWRITE_PNG_COMPRESSION, 0])
        if success:
            if image_msg.header.seq % 5 == 0:
                img_str = base64.b64encode(content).decode()
                self.client.publish(mqtt_topic, img_str)
                ct = int(time.time())
                #self.get_logger().info("Video scene sent with DIFF" +  str(image_msg.header.stamp.secs) + " sec" + str(image_msg.header.seq))


def main(args=None):
    rclpy.init(args=args)
    node = MqttVideoStreamer(
        keepalive=60
    )
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
