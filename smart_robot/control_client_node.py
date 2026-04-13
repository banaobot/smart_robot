from platform import node

import rclpy
from rclpy.node import Node
from std_srvs.srv import SetBool


class ControlClientNode(Node):

  def __init__(self):
    super().__init__('control_client_node')

    # Create client
    self.client = self.create_client(SetBool, 'robot_control')
    # Wait for service
    while not self.client.wait_for_service(timeout_sec=1.0):
      self.get_logger().info('Waiting for service...')

    self.get_logger().info("Control Client Node Started")
    self.send_requests()

  def send_requests(self):

    while True:
      user_input = input("\nEnter command (start/stop/exit): ").strip().lower()

      if user_input == "exit":
        self.get_logger().info("Exiting Control Client Node...")
        self.destroy_node() 
        # Raising SystemExit is the cleanest way to break out of rclpy.spin()
        raise SystemExit 
      
      if user_input not in ["start", "stop"]:
        print("Invalid command!")
        continue

      request = SetBool.Request()
      request.data = True if user_input == "start" else False
      future = self.client.call_async(request)
      # Wait for response
      rclpy.spin_until_future_complete(self, future)
      response = future.result()
      self.get_logger().info(f"Response: {response.message}")

def main(args=None):
	rclpy.init(args=args)
	node = ControlClientNode()
	try:
		rclpy.spin(node)
	except KeyboardInterrupt:
		pass
	finally:
		node.destroy_node()
		try:
			rclpy.shutdown()
		except:
			pass

if __name__ == '__main__':
    main()