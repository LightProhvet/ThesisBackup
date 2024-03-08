"""
Aruco tag detection from image, position assessment from the tags.

@input: Camera color image
@output: When Aruco tag is seen publishes the tag id in ROS topic and publishes the TF tranformation of a helper entity
    sensor_detected_camera_link that will make possible the other TF data to be adjusted.
"""

import numpy as np
import math
import cv2
import cv_bridge
import cv2.aruco as aruco
import rclpy
from rclpy.node import Node
from rclpy.parameter import Parameter

import tf2_ros
from sensor_msgs.msg import Image
from robot_ros2_msgs.msg import Tag
from geometry_msgs.msg import TransformStamped
import copy
from tf_transformations import euler_from_quaternion, quaternion_from_matrix

class ReadAruco(Node):
    def __init__(self, filename, aruco_size = 0.096):
        super().__init__('ReadAruco')
        self.get_logger().info("---------------------------------------------------------")
        self.get_logger().info("camera_shape:")
        self.arucoSize = aruco_size
        self.filename = filename
        self.foundCalibration = False
        self.isInitialized = False
        self.pose_pub = self.create_publisher(Tag, "arucoTag", 3)
        self.debug_img_pub = self.create_publisher(Image, "aruco_debug_img", 0)

        self.tagMsg = Tag()

        # Transform broadcaster
        self.transform_broadcaster = tf2_ros.TransformBroadcaster(self)
        self.transform_msg = TransformStamped()
        
        self.declare_parameter("camera_shape.data", Parameter.Type.DOUBLE_ARRAY)
        self.declare_parameter("camera_matrix.data", Parameter.Type.DOUBLE_ARRAY)
        self.declare_parameter("distortion_coefficients.data", Parameter.Type.DOUBLE_ARRAY)
        
        self.get_logger().info("------------------------------- ARUCO INIT FINISHED ---------------------------------")

        #self.arucos_floors = self.declare_parameter("arucos_floors", Parameter.Type.NOT_SET) #existing aruco ID-s and floor on which they are located
        
        # TODO: Fix the ReadAruco node
        #self.create_timer(0.1, self.detect)

    def initialize(self, threshold):
        if(self.foundCalibration):
            self.aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_6X6_250)
            # detector parameters can be set here (List of detection parameters[3])
            self.parameters = aruco.DetectorParameters()
            self.detector = aruco.ArucoDetector(self.aruco_dict, self.parameters)
            self.parameters.adaptiveThreshConstant = threshold
            self.isInitialized = True

    def detect(self, image):
        if(self.foundCalibration == False):
            try:
                #calibration_file = cv2.FileStorage(self.filename, cv2.FILE_STORAGE_READ)
                
                self.camera_shape = np.array(self.get_parameter_or("camera_shape.data", []).value)
                self.camera_matrix = np.array(self.get_parameter_or("camera_matrix.data", []).value)
                self.camera_matrix = self.camera_matrix.reshape((3, 3))
                self.camera_distortion_coefficients = np.array(self.get_parameter_or("distortion_coefficients.data", []).value)
                #calibration_file.release()
                self.foundCalibration = True
                
                self.get_logger().info("Aruco reader has found the camera calibration parameters")
                self.get_logger().info("---------------------------------------------------------")
                self.get_logger().info("camera_shape:")
                self.get_logger().info(str(self.camera_shape))
                self.get_logger().info("---------------------------------------------------------")
                self.get_logger().info("camera_matrix:")
                self.get_logger().info(str(self.camera_matrix))
                self.get_logger().info("---------------------------------------------------------")
                self.get_logger().info("camera_distortion_coefficients:")
                self.get_logger().info(str(self.camera_distortion_coefficients))
                self.get_logger().info("---------------------------------------------------------")
        
            except:
                raise
                self.get_logger().info("Camera calibration not found!")
                
        if(self.isInitialized):
            # lists of ids and the corners belonging to each id
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            corners, ids, rejectedImgPoints = self.detector.detectMarkers(gray, self.aruco_dict, parameters=self.parameters)
            aruco_image = copy.copy(image)
            # font for displaying text (below)
            font = cv2.FONT_HERSHEY_SIMPLEX

            # check if the ids list is not empty
            # if no check is added the code will crash
            if np.all(ids != None):

                #Find and drop Aruco codes that are not in our dictionary
                to_delete = []
                for i in range(len(ids)):
                    if str(ids[i][0]) not in self.arucos_floors:
                        to_delete.append(i)
                ids = np.delete(ids, to_delete, 0)
                corners = np.delete(corners, to_delete, 0)

                # If more than one marker visible, find which one is closest - biggest distance between it's corners.
                best = 0
                if len(corners) > 1:
                    biggest_length = 0
                    for i, corners_set in enumerate(corners):
                        for j in range(-1, 3):
                            side_length = math.sqrt(
                                (corners_set[0][j][0] - corners_set[0][j + 1][0]) ** 2 +
                                (corners_set[0][j][1] - corners_set[0][j + 1][1]) ** 2
                            )
                            if side_length > biggest_length:
                                biggest_length = side_length
                                best = i

                if len(ids) > 0:
                    # Use line 1 if you get error related to number of values to unpack.
                    rvec, tvec, _ = aruco.estimatePoseSingleMarkers(corners, self.arucoSize, self.camera_matrix, self.camera_distortion_coefficients)
                    #rvec, tvec = aruco.estimatePoseSingleMarkers(corners, self.arucoSize, self.camera_matrix, self.camera_distortion_coefficients)
                    #rvecs_list = []
                    tvecs_list = []
                    for i in range(len(rvec)):
                        rvec_rs, tvec_rs = rvec[0].reshape((3, 1)), tvec[0].reshape((3, 1))
                        #rvecs_list.append(rvec_rs)
                        tvecs_list.append(tvec_rs)

                    #TODO search among the found arucos if we see the next one or any of the next ones (in order)
                    # of the markers that are supposed to form current route.
                    # If the seen marker is not on current route, investigate where it is and try to correct route.

                    #self.get_logger().info("tvec:", round(tvecs_list[0][0][0], 2), round(tvecs_list[0][1][0], 2), round(tvecs_list[0][2][0], 2), "rvec:",
                    #      round(rvecs_list[0][0][0], 2), round(rvecs_list[0][1][0], 2), round(rvecs_list[0][2][0], 2))

                    rotation_matrix_one, _ = cv2.Rodrigues(rvec[best])
                    rotation_matrix_two = cv2.transpose(rotation_matrix_one)
                    inv_tvec = -1* rotation_matrix_two @ tvecs_list[best]

                    rotation_matrix = np.array([
                        [1, 0, 0, inv_tvec[0]],
                        [0, 1, 0, inv_tvec[1]],
                        [0, 0, 1, inv_tvec[2]],
                        [0, 0, 0, 1]],
                        dtype=float)
                    rotation_matrix[:3,:3] = rotation_matrix_two

                    #self.get_logger().info("inv_tvec: ", inv_tvec)

                    # convert the matrix to a quaternion
                    quaternion = quaternion_from_matrix(rotation_matrix)

                    distance = math.sqrt(math.pow(tvecs_list[best][0], 2) + math.pow(tvecs_list[best][1], 2))
                                # distance of camera on x-y plane of aruco on floor, so the robot base's distance can be
                                # assessed from it
                    #(rvec-tvec).any() # get rid of that nasty numpy value array error

                    for i in range(0, ids.size):
                        # draw axis for the aruco markers
                        aruco.drawAxis(aruco_image, self.camera_matrix, self.camera_distortion_coefficients, rvec[i], tvec[i], 0.1)

                    # draw a square around the markers
                    aruco.drawDetectedMarkers(aruco_image, corners)

                    # code to show ids of the marker found
                    strg = ''
                    for i in range(0, ids.size):
                        if i == best:
                            strg += "["
                        strg += str(ids[i][0])
                        if i == best:
                            strg += "]"
                        strg +=','

                    textcolor = (0, 0, 255)  # Red text on visualization window if position calculation end up not okay

                    # Check if the computed TF is realistic taking into account that the markers are on floor and
                    # camera angle is fixed.
                    # Explanation of the ambiguous computations: https://github.com/opencv/opencv/issues/8813
                    x_angle, y_angle, z_angle = euler_from_quaternion([quaternion[0],
                                                                     quaternion[1],
                                                                     quaternion[2],
                                                                     quaternion[3]])

                    if x_angle < 0:  # If camera postition in aruco frame has x angle negative then the computation is right, publish

                        textcolor = (0, 255, 0)  # Green text on visualization window if position calculation is okay

                        self.tagMsg.ID = ids[best][0]
                        '''self.tagMsg.pose.position.x = tvecs_list[best][0]
                        self.tagMsg.pose.position.y = tvecs_list[best][1]
                        self.tagMsg.pose.position.z = tvecs_list[best][2]
                        self.tagMsg.pose.orientation.x = quaternion[0]
                        self.tagMsg.pose.orientation.y = quaternion[1]
                        self.tagMsg.pose.orientation.z = quaternion[2]
                        self.tagMsg.pose.orientation.w = quaternion[3]'''
                        self.tagMsg.distance = distance
                        self.tagMsg.floor = self.arucos_floors[str(ids[best][0])]
                        self.pose_pub.publish(self.tagMsg)

                        #self.get_logger().info(self.tagMsg.pose.position.x, self.tagMsg.pose.position.y, self.tagMsg.pose.position.z, self.tagMsg.distance)'''

                        self.transform_msg.header.stamp = self.get_clock().now().to_msg()
                        self.transform_msg.header.frame_id = "aruco" + str(ids[best][0])
                        self.transform_msg.child_frame_id = "sensor_calculated_camera_link"
                        self.transform_msg.transform.translation.x = inv_tvec[0]
                        self.transform_msg.transform.translation.y = inv_tvec[1]
                        self.transform_msg.transform.translation.z = inv_tvec[2]
                        self.transform_msg.transform.rotation.x = quaternion[0]
                        self.transform_msg.transform.rotation.y = quaternion[1]
                        self.transform_msg.transform.rotation.z = quaternion[2]
                        self.transform_msg.transform.rotation.w = quaternion[3]

                        self.transform_broadcaster.sendTransform(self.transform_msg)

                    cv2.putText(aruco_image, "Id: " + strg, (0, 64), font, 1, textcolor, 2, cv2.LINE_AA)

                    min_x = min([corner[0] for corner in corners[0][0]])
                    max_x = max([corner[0] for corner in corners[0][0]])
                    min_y = min([corner[1] for corner in corners[0][0]])
                    max_y = max([corner[1] for corner in corners[0][0]])
                    center_x = (min_x + max_x) / 2
                    center_y = (min_y + max_y) / 2
                    image_x_min = max(0, int(center_x-50))
                    image_x_max = min(640, int(center_x+50))
                    image_y_min = max(0, int(center_y - 50))
                    image_y_max = min(480, int(center_y + 50))
                    if image_x_max - image_x_min < 100:
                        if image_x_max == 640:
                            image_x_min = 640 - 100
                        else:
                            image_x_max = 100
                    if image_y_max - image_y_min < 100:
                        if image_y_max == 480:
                            image_y_min = 480 - 100
                        else:
                            image_y_max = 100
                    debug_image = aruco_image[image_y_min:image_y_max, image_x_min:image_x_max]
                    #cv2.imshow('Detected Arucos', debug_image)
                    img_msg = cv_bridge.CvBridge().cv2_to_imgmsg(debug_image, encoding='bgr8')
                    self.debug_img_pub.publish(img_msg)
                    #cv2.imshow('Detected Arucos', aruco_image)
                    #cv2.waitKey(2)

def main(args=None):
        rclpy.init(args=args)
        node = ReadAruco(10, 'yellow') #  'yellow' is currently ignored TODO
        rclpy.spin(node)
        rclpy.shutdown()

if __name__ == '__main__':
    main()



                    

