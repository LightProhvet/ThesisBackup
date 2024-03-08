

# import threading

import numpy as np

import rclpy  # import rospy
from rclpy.node import Node
from rclpy.parameter import Parameter


from semantic_segmentation.cv_bridge import imgmsg_to_cv2, cv2_to_imgmsg
from sensor_msgs.msg import Image  # still valid


class SegmentationNode(Node):

    def __init__(self):
        super().__init__('SegmentationNode')

        self.declare_parameter("segmentation_model", 'deeplabv3_test')
        self.declare_parameter("rate", Parameter.Type.DOUBLE)

        # this should be also in callback?
        seg_model_name = self.get_parameter('segmentation_model').get_parameter_value().string_value
        # rate = self.get_parameter("rate").get_parameter_value()
        # we need these fields for reverse-compatibility? params would be enough?
        # MODEL -> MODEL_NAME
        self.MODEL_NAME = seg_model_name  # rospy.get_param('~model', 'mnv2_bdd100k_driveable_513')
        self.TOPIC_IMAGE = 'image_raw'
        self.TOPIC_SEMANTIC = 'semantic'
        self.TOPIC_SEMANTIC_COLOR = 'semantic_color'
        # self.RATE = rate  # rospy.get_param('~rate', 30.0)

        # self.subscription = self.create_subscription(String, 'topic', self.listener_callback, 10)
#        sub_image = rospy.Subscriber(TOPIC_IMAGE, Image, on_image)
        self.sub_image = self.create_subscription(Image, self.TOPIC_IMAGE, self.on_image, 10 )
    # elf.self.publisher_ = self.create_publisher(String, 'topic', 10)
        self.pub_semantic = self.create_publisher(Image, self.TOPIC_SEMANTIC, 1)
        self.pub_semantic_color = self.create_publisher(Image, self.TOPIC_SEMANTIC_COLOR, 1)
        self.model = self.get_model()
        self.last_image = None

        self.declare_parameter("semantic_categories", self.model.get_categories())
        # self.semantic_categories =  self.get_parameter('semantic_categories').get_parameter_value()

    # returns the actual model (instead of its name)
    def get_model(self):
        # the models are put into the same folder after building.
        model = getattr(__import__('models', globals(), locals(), fromlist=[self.MODEL_NAME]), self.MODEL_NAME).Model()
        return model

    def on_image(self, msg):
        self.last_image = msg
        self.get_logger().info('Received message for segmentation')
        self.segmentation_callback()
    """
    The data comes into the callback as a numpy array (numpy.ndarray), 
    the specific format depends on external factors (e.g sensors and their managment packages)
    While only infer() function is needed for Model to work. Preprocessing is highly recommended. 
    """
    def segmentation_callback(self):
        # model = getattr(__import__('models', globals(), locals(), fromlist=[MODEL_NAME]), MODEL_NAME).Model()
        model = self.get_model()  # should we save this in the class so callback wouldn't have to waste time on this?
        # rospy.set_param("semantic_categories", model.categories)
        try:
            # while rclpy.ok():  # not rospy.is_shutdown():
            if self.last_image is None:
                return
            image = self.last_image
            images = [imgmsg_to_cv2(image)]
            images = [i.astype(np.float32) for i in images]

            header = self.last_image.header
            self.get_logger().info(f'Starting infer: {images[0].shape}')
            semantic = model.infer(images)[0]
            self.get_logger().info(f'Infer complete: {semantic}')
            self.get_logger().info(f'Infer complete: {semantic.shape}')
            self.last_image = None
            # if self.count_subscribers(self.TOPIC_SEMANTIC) > 0
            self.get_logger().info(f'Ready to publish semantic: {self.pub_semantic.get_subscription_count()}')
            self.get_logger().info(f'Ready to publish semantic color: {self.pub_semantic_color.get_subscription_count()}')

            if self.pub_semantic.get_subscription_count() > 0:  # self.pub_semantic.get_num_connections() > 0:
                m = cv2_to_imgmsg(semantic.astype(np.uint8), encoding='rgb8')
                m.header.stamp.sec = header.stamp.sec
                m.header.stamp.nanosec = header.stamp.nanosec
                self.pub_semantic.publish(m)

            # if self.pub_semantic_color.get_subscription_count() > 0:  # get_num_connections() > 0:
            #     m = cv2_to_imgmsg(model.color_map[semantic.astype(np.uint8)], encoding='rgb8')
            #     m.header.stamp.sec = header.stamp.sec
            #     m.header.stamp.nsec = header.stamp.nsec
            #     self.pub_semantic_color.publish(m)
        except KeyboardInterrupt:
            pass


def main(args=None):
    rclpy.init(args=args)
    segmentation_node = SegmentationNode()
    # rate = rospy.Rate(RATE)
    # rate = segmentation_node.create_rate(segmentation_node.RATE)
    # rate.sleep()
    # see https://github.com/ros2/rclpy/blob/75c51c945d6029bea61571ced43c1d1b9c3c6703/rclpy/test/test_rate.py on how to implement rate ensurance
    # Spin in a separate thread to ensure rate
    # thread = threading.Thread(target=rclpy.spin, args=(segmentation_node,), daemon=True)
    # thread.start()

    rclpy.spin(segmentation_node)

    segmentation_node.destroy_node()
    rclpy.shutdown()
    # thread.join()


if __name__ == '__main__':
    main()

