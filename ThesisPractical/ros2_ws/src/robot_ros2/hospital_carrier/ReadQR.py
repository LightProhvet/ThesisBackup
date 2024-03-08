#!/usr/bin/env python



"""
@author: Walid Remmas
@input: Image from camera
@output: Global pose
Class that updates localization based on tags
"""
# pip install: "pip install pyzbar"
# Library for qr code reading
import pyzbar.pyzbar as pyzbar 


import math
import rclpy
from rclpy.node import Node
import numpy as np
import cv2
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image


class TagReader(Node):
	def __init__(self, rate):
		super().__init__('TagReader')
		self.bridge = CvBridge()
		# Subscribers
		self.tag_sub = self.create_subscription(Image, "/camera/color/image_raw", self.onImage, 10)

		self.previousTag = 0
		self.tagID = 0
		self.location = (None, None)
		self.floorNumber = None
		self.tagOrientation = None

		self.rate = self.create_rate(rate)
		self.timer = self.create_timer(0.1, self.run)

	def run(self):
		"""
		Main loop of class.
		@param: self
		@result: runs the step function for localizer update
		"""
		self.step()
		#self.rate.sleep()


	def step(self):
		"""
		Perform an iteration of the qr code reading.
		@param: self
		@result: updates and publishes pose estimation of 
		the vehicle globally and relative to the
		next waypoint. 
		"""

		if self.tagID != self.previousTag:
			self.get_logger().info('Found new tag:')
			self.get_logger().info('---------------')
			self.get_logger().info('Tag-ID: ' + str(self.tagID))
			self.get_logger().info('Location: ' + str(self.location))
			self.get_logger().info('Tag-orientation: ' +  str(self.tagOrientation))
			self.get_logger().info('floorNumber: ' +  str(self.floorNumber))
			self.get_logger().info('---------------')
			self.previousTag = self.tagID

	def onImage(self, image_raw):
		"""
		Handles incoming tag information messages.
		@param: self
		@param: image - raw color image from camera 
		@result: QR code location and info
		"""
		try:
			cv_image = self.bridge.imgmsg_to_cv2(image_raw, "bgr8")
		except CvBridgeError as e:
			self.get_logger().info(str(e))

		decodedObjects = self.decode(cv_image)
		self.display(cv_image, decodedObjects)

		
		

	def decode(self, image):
		# Find barcodes and QR codes
		decodedObjects = pyzbar.decode(image)

		# Print results
		for obj in decodedObjects:
			textFromQR = str(obj.data) 
			dataFromText = textFromQR.splitlines()
			self.location = (float(dataFromText[1]), float(dataFromText[2])) 
			self.floorNumber = dataFromText[3]
			self.tagOrientation = float(dataFromText[4])
			self.tagID = dataFromText[6]

		return decodedObjects


	# Display barcode and QR code location
	def display(self, im, decodedObjects):
		foundCode = 0
		# Loop over all decoded objects
		for decodedObject in decodedObjects:
			points = decodedObject.polygon
			foundCode = 1

		if foundCode:
			# If the points do not form a quad, find convex hull
			if len(points) > 4 :
				hull = cv2.convexHull(np.array([point for point in points], dtype=np.float32))
				hull = list(map(tuple, np.squeeze(hull)))
			else :
				hull = points

			# Number of points in the convex hull
			n = len(hull)

			# Draw the convext hull
			for j in range(0,n):
				cv2.line(im, hull[j], hull[ (j+1) % n], (255,0,0), 3)

		# Display results
		cv2.imshow("Results", im)
		cv2.waitKey(2)	

		return decodedObjects	

def main(args=None):
	rclpy.init(args=args)
	node = TagReader(10)
	rclpy.spin(node)
	rclpy.shutdown()

if __name__ == '__main__':
	main()
