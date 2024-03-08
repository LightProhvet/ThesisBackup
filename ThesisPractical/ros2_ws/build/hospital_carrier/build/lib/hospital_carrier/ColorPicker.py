#!/usr/bin/env python

"""
@author: Walid REMMAS
@contact: remmas.walid@gmail.com
          +33 6 62 55 45 04
"""

import rclpy
from rclpy.node import Node
from rclpy.timer import Rate
from geometry_msgs.msg import Point
from sensor_msgs.msg import Image

import cv2
from cv_bridge import CvBridge, CvBridgeError

import numpy as np

class ColorPicker(Node):
	def __init__(self):
		super.__init__('ColorPicker')
		self.done = 0
		self.selected = 0
		self.r = (0, 0, 0, 0)
		self.imCrop = None
		self.camera = None
		self.color_msg = Point()
		self.bridge = CvBridge()
		self.camera_sub = self.create_subscription(Image, "/camera/color/image_raw", self.onCamera, 10)
		#self.color_pub = self.create_subscription(Point, "color", queue_size=10, 10)
	
	def onCamera(self, image):
		try:
			cv_image = self.bridge.imgmsg_to_cv2(image, desired_encoding='bgr8')
		#image_message = cv2_to_imgmsg(cv_image, encoding="passthrough")	
		except CvBridgeError as e:
			self.get_logger().info(e)   
		
		self.camera = cv_image
		if self.done == 0:
			if not self.selected:
				if self.r == (0, 0, 0, 0):
					self.r = cv2.selectROI(cv_image)
					#self.get_logger().info(r)
					# Crop image
					self.imCrop = cv_image[int(self.r[1]):int(self.r[1]+self.r[3]), int(self.r[0]):int(self.r[0]+self.r[2])]
					return
				self.selected = 1
				cv2.destroyAllWindows()
			elif self.selected:
				b,g,r,_=np.uint8(cv2.mean(self.imCrop))
				color=cv2.cvtColor(np.uint8([[[b,g,r]]]),cv2.COLOR_BGR2HSV)
				#self.get_logger().info(color)
				h= color[0][0][0]
				s= color[0][0][1]
				v= color[0][0][2]
				self.color_msg.x = h
				self.color_msg.y = s
				self.color_msg.z = v
				#self.color_pub.publish(self.color_msg)
				self.done = 1
				self.get_logger().info('Picked color HSV : ')
		else:
			#self.color_pub.publish(self.color_msg)
			self.get_logger().info(str(self.color_msg.x) + str(self.color_msg.y) + str(self.color_msg.z))

def main(args=None):
    rclpy.init(args=args)
    node = ColorPicker()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__=="__main__":
	main()

