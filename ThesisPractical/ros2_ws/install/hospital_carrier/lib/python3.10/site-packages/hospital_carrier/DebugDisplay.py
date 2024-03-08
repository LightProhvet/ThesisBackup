#!/usr/bin/env python3

"""
@author: Anna J&otilde;gi
"""

import cv2, cv_bridge
import rclpy
from rclpy.node import Node

from std_msgs.msg import Bool, String, Int32, Int16
from sensor_msgs.msg import Image
from robot_ros2_msgs.msg import IntList, Tag
import numpy as np
import tf2_ros
import time
import os

class DebugDisplay(Node):
    def __init__(self, rate):
        # initialize relevant opencv structures
        super().__init__('DebugDisplay')
        self.bridge = cv_bridge.CvBridge()

        #Subscribers
        self.main_image_sub = self.create_subscription(Image, "camera_stream2", self.onImage, 10)
        self.aruco_image_sub = self.create_subscription(Image, "aruco_debug_img", self.onArucoImage, 10)
        self.obst_dists_on_paths_sub = self.create_subscription(IntList, "obst_dists_on_paths", self.onObstDists, 10)
        self.op_mode_sub = self.create_subscription(String, "op_mode", self.onOpMode, 10)
        self.tag_sub = self.create_subscription(Tag, "arucoTag", self.onTag, 10)
        self.line_sub = self.create_subscription(Bool, "is_line", self.onLine, 10)
        self.debug_line_sector_sub = self.create_subscription(Int16, "debug_line_sector", self.onSector, 10)
        self.debug_path_sub = self.create_subscription(Int16, "debug_path", self.onPath, 10)
        self.debug_state_sub = self.create_subscription(String, "debug_state", self.onState, 10)

        # Transform listener
        self.tfBuffer = tf2_ros.Buffer()
        self.listener = tf2_ros.TransformListener(self.tfBuffer, self)

        #full_path = os.path.realpath(__file__)
        #TODO: Saa kuidagi ros2 workspace path kätte relatiivselt
        self.background = cv2.imread('/home/robot/robot_ros2/src/robot_ros2/debug_images/background.png')

        self.op_mode = ""
        self.x = ""
        self.y = ""
        self.floor = ""

        self.image = []
        self.aruco_image = []
        self.image_time = 0
        self.aruco_image_time = 0
        self.obst_distances = np.zeros(7)
        self.line_sector = -1
        self.chosen_path = -1
        self.state_info = ""

        self.overlay_images = [[], [], [], [], [], [], []]
        #full_path = os.path.realpath(__file__)
        for i in range(7):
            with open('/home/robot/robot_ros2/src/robot_ros2/debug_images/pathmask_' + str(i) + '.pbm', "r") as f:
                lines = f.readlines()
                img_arr = []
                row_arr = []
                c = 0
                for line in lines[3:]:
                    for char in line:
                        if char != '\n':
                            row_arr.append([int(char) * 200, 0, int(char) * 255])
                            c = c + 1
                            if c == 640:
                                c = 0
                                img_arr.append(row_arr)
                                row_arr = []

                self.overlay_images[i] = np.array(img_arr, dtype=np.uint8)

        self.rate = self.create_rate(rate)
        self.timer = self.create_timer(0.1, self.run)

    def onImage(self, msg):
        self.image = cv_bridge.CvBridge().imgmsg_to_cv2(msg, desired_encoding='passthrough')
        self.image_time = time.time()

    def onArucoImage(self, msg):
        self.aruco_image = cv_bridge.CvBridge().imgmsg_to_cv2(msg, desired_encoding='passthrough')
        self.aruco_image_time = time.time()

    def onObstDists(self, obst_dists_msg):
        for i, val in enumerate(obst_dists_msg.data):
            self.obst_distances[i] = val / 1000  # Convert from mm to m

    def onOpMode(self, op_mode_msg):
        self.op_mode = op_mode_msg.data
        self.state_info = ""

    def onTag(self, tag_msg):
        self.floor = str(tag_msg.floor)

    def onLine(self, line_msg):
        self.is_line = line_msg

    def onLocalization(self, localizer_msg):
        self.x = localizer_msg.x
        self.y = localizer_msg.y

    def onSector(self, msg):
        self.line_sector = msg.data

    def onPath(self, msg):
        self.chosen_path = msg.data

    def onState(self, msg):
        self.state_info = msg.data

    def run(self):
        self.step()
        #self.rate.sleep()

    def step(self):
        error = False
        try:
            transform = self.tfBuffer.lookup_transform('map', 'base_footprint', self.get_clock().now())
        except (tf2_ros.LookupException, tf2_ros.ConnectivityException, tf2_ros.ExtrapolationException) as e:
            error = True

        if not error:
            self.x = str("{:.2f}".format(transform.transform.translation.x))
            self.y = str("{:.2f}".format(transform.transform.translation.y))

        frame = self.background.copy()
        font = cv2.FONT_HERSHEY_PLAIN
        textcolor = (255, 255, 255)
        # Write robot location and operation mode related info
        cv2.putText(frame, "Op mode: " + self.op_mode,
                    (650, 22), font, 1, textcolor, 1, cv2.LINE_AA)
        cv2.putText(frame, "Robot location X: " + self.x + " Y: " + self.y,
                   (650, 34), font, 1, textcolor, 1, cv2.LINE_AA)
        cv2.putText(frame, "floor: " + self.floor,
                    (680, 46), font, 1, textcolor, 1, cv2.LINE_AA)
        cv2.putText(frame, self.state_info,
                    (650, 58), font, 1, textcolor, 1, cv2.LINE_AA)

        # Draw chosen path over image
        main_image = self.image.copy()
        if self.chosen_path > -1:
            overlay = self.overlay_images[self.chosen_path]
            main_image = cv2.addWeighted(main_image, 1, overlay, 1, 0)
        # Add main image to background
        if len(main_image) > 0 and self.image_time > time.time() - 1:
            frame[0:480, 0:640] = main_image

        # Draw obstacle distance bars
        for i in range(7):
            bar_color = (0,0,0)
            height = int(max(150-self.obst_distances[i]*100, 0))
            cv2.rectangle(frame, (775 + i * 25, 160), (775 + (i+1) * 25, 160+height), bar_color, -1)
        # Draw indicator of sector that has line if relevant
        if self.op_mode == "follower":
            if self.line_sector >= 0:
                cv2.rectangle(frame, (775 + self.line_sector * 25, 311), (775 + (self.line_sector + 1) * 25, 320), (0, 100, 100), -1)
                cv2.putText(frame, "Line detected:",
                            (650, 320), font, 1, textcolor, 1, cv2.LINE_AA)
            else:
                cv2.putText(frame, "No line",
                            (650, 320), font, 1, textcolor, 1, cv2.LINE_AA)
        # Add aruco image if available, and ID
        if len(self.aruco_image) > 0 and self.aruco_image_time > time.time() - 1:
            frame[330:430, 850:950] = self.aruco_image
        # Show the window
        cv2.imshow('Robot', frame)
        cv2.waitKey(2)


def main(args=None):
    rclpy.init(args=args)
    node = DebugDisplay(5)
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()