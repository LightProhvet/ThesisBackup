#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from rclpy.parameter import Parameter

from std_msgs.msg import String
import paho.mqtt.client as mqtt
import json

class MqttListener(Node):
    def __init__(self, keepalive):
        super().__init__('MqttListener')

        #Parameters
        self.declare_parameter('host', Parameter.Type.STRING)
        self.declare_parameter('port', Parameter.Type.INTEGER)
        self.declare_parameter('username', Parameter.Type.STRING)
        self.declare_parameter('password', Parameter.Type.STRING)
        self.declare_parameter('listen_topic_destination', Parameter.Type.STRING)
        self.declare_parameter('listen_topic_remotecontrol', Parameter.Type.STRING)
        self.declare_parameter('ca_file', Parameter.Type.STRING)

        self.host = self.get_parameter('host').value
        self.port = self.get_parameter('port').value
        self.username = self.get_parameter('username').value
        self.password = self.get_parameter('password').value
        self.topic_destination = self.get_parameter('listen_topic_destination').value
        self.topic_remotecontrol = self.get_parameter('listen_topic_remotecontrol').value
        self.ca_file = self.get_parameter('ca_file').value
        self.keepalive = keepalive
        
        self.client = mqtt.Client()
        self.client.username_pw_set(username=self.username, password=self.password)
        self.client.tls_set(ca_certs=self.ca_file)
        self.client.tls_insecure_set(True)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

        # Publishers
        self.mqtt_topic_destination_pub = self.create_publisher(String, "mqtt_destination_command", 1)
        self.mqtt_topic_destination_cancel_pub = self.create_publisher(String, "mqtt_destination_cancel", 1)
        self.mqtt_topic_remotecontrol_pub = self.create_publisher(String, "mqtt_remote_control_move", 1)

        self.timer = self.create_timer(0.1, self.run)
        
        if not rclpy.ok():
            self.client.disconnect()
            self.client.loop_stop()

    def run(self):
        self.client.connect(self.host, self.port, self.keepalive)
        self.client.loop_start()
        self.client.subscribe(self.topic_remotecontrol)
        self.client.subscribe(self.topic_destination)
        self.client.subscribe('#')
        #rclpy.spin(self)
        #rclpy.shutdown()

    def on_connect(self, client, userdata, flags, rc):
        self.get_logger().info("MqttListener node mqtt client connected with result code "+str(rc))

    def on_message(self, client, userdata, message):
        self.get_logger().info("On topic " + str(message.topic) + " message received:" + str(message.payload.decode("utf-8")))
        if message.topic == self.topic_destination:
            parsed = json.loads(message.payload.decode("utF-8").replace('\'', '"'))
            if parsed["command"]["action"] is not None and parsed["command"]["action"] == "goto":
                if parsed["command"]["from"] is not None and parsed["command"]["to"] is not None:
                    route_name = "location" + parsed["command"]["from"] + "-location" + parsed["command"]["to"]
                    self.mqtt_topic_destination_pub.publish(route_name)
        elif message.topic == self.topic_remotecontrol:
            message_str = message.payload.decode("utf-8")
            move_dir = False
            if '["rotate-right"]' in message_str:
                move_dir = "rotate-right"
            elif '["rotate-left"]' in message_str:
                move_dir = "rotate-left"
            elif '["up"]' in message_str:
                move_dir = "up"
            elif '["down"]' in message_str:
                move_dir = "down"
            elif '["right"]' in message_str:
                move_dir = "right"
            elif '["left"]' in message_str:
                move_dir = "left"
            if move_dir:
                self.mqtt_topic_remotecontrol_pub.publish(move_dir)

        '''
        message_str = message.payload.decode("utf-8")
            if message_str == "cancel":
                self.mqtt_topic_destination_cancel_pub(message_str)
            else:
                self.mqtt_topic_destination_pub.publish(message_str)'
                
        else:
            self.get_logger().info("On topic ", message.topic , " message received: " , str(message.payload.decode("utf-8")))
        '''

def main(args=None):
    rclpy.init(args=args)

    node = MqttListener(
        keepalive=60
    )
    
    try:
        rclpy.spin(node)
        rclpy.shutdown()
    except:
        print("MQTT remote control listener failed to connect.")

if __name__ == '__main__':
    main()

