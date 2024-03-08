import subprocess
import rclpy
from rclpy.node import Node
from rclpy.parameter import Parameter
from sensor_msgs.msg import PointCloud2
import open3d as o3d
from .open3d_ros_helper import rospc_to_o3dpc
# https://github.com/felixchenfy/open3d_ros_pointcloud_conversion/blob/master/lib_cloud_conversion_between_Open3D_and_ROS.py

class PointcloudToPly(Node):
    def __init__(self):
        super().__init__("PointcloudToPly")

        # Subscribers
        self.pcl_sub = self.create_subscription(PointCloud2, "/camera/depth/color/points", self.onPointCloud, 10)
        
        #Parameters
        self.declare_parameter("model_path", Parameter.Type.STRING)
        self.declare_parameter("output_path", Parameter.Type.STRING)
        self.declare_parameter("data_dir", Parameter.Type.STRING)

        self.model_path = self.get_parameter("model_path").value
        self.output_path = self.get_parameter("output_path").value
        self.data_dir = self.get_parameter("data_dir").value
        self.point_cloud = PointCloud2()
        self.formatted_data = None
    
        self.create_timer(0.1, self.run)

    def run(self):
        # Code to feed the data to the mapmos model. Haven't been able to test it yet so remove the first if you're ready to test.
        if self.formatted_data is not None:
            process = subprocess.Popen(['mapmos_pipeline', '--visualize', self.model_path, self.data_dir], 
                                       stdout=subprocess.PIPE, universal_newlines=True)
            while True:
                output = process.stdout.readline()
                self.get_logger().info(output.strip())
                return_code = process.poll()
                if return_code is not None:
                    self.get_logger().info(f'RETURN CODE {return_code}')
                    #Process finished, log rest of the lines
                    for output in process.stdout.readlines():
                        self.get_logger().info(output.strip())
                    break
                    


    def onPointCloud(self, pcl_msg: PointCloud2):
        o3d_cloud = rospc_to_o3dpc(pcl_msg)
        o3d.io.write_point_cloud(self.output_path, o3d_cloud)

def main(args=None):
    rclpy.init(args=args)
    node = PointcloudToPly()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
	main()