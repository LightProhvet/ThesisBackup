import sys
from threading import Thread

from example_interfaces.srv import AddTwoInts
import rclpy
from rclpy.node import Node


class MinimalClient(Node):

    def __init__(self):
        super().__init__('minimal_client_async')
        self.cli = self.create_client(AddTwoInts, 'add_two_ints')
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('service not available, waiting again for server...')
        self.req = AddTwoInts.Request()

    def send_request_async(self, a, b):
        self.req.a = a
        self.req.b = b
        self.future = self.cli.call_async(self.req)
        rclpy.spin_until_future_complete(self, self.future)
        return self.future.result()

    # haven't tested how this causes a deadlock, but it should.
    def send_request_sync_wrong(self, a, b):
        self.req.a = a
        self.req.b = b
        self.future = self.cli.call(self.req)
        rclpy.spin_until_future_complete(self, self.future)
        return self.future.result()

    def send_request_sync(self):
        self.req.a = int(sys.argv[1])
        self.req.b = int(sys.argv[2])
        return self.cli.call(self.req)


def main():
    rclpy.init()
    minimal_client = MinimalClient()

    spin_thread = Thread(target=rclpy.spin, args=(minimal_client,))
    spin_thread.start()
    # input1 = int(sys.argv[1])
    # input2 = int(sys.argv[2])
    # response_async = minimal_client.send_request_async(input1, input2)
    # minimal_client.get_logger().info(f'Result of add_two_ints: for {input1} + {input2} = {response.sum}')
    response = minimal_client.send_request_sync()
    minimal_client.get_logger().info(f'Result of add_two_ints: for {minimal_client.req.a} + {minimal_client.req.b} = {response.sum}')

    minimal_client.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
