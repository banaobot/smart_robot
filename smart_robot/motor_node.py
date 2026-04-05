import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class MotorNode(Node):
    
	def __init__(self):
		super().__init__('motor_node')

		self.subscription = self.create_subscription(String, '/cmd_vel', self.command_callback, 10)
		self.get_logger().info("Motor Node Started")
                
	def command_callback(self, msg):
		command = msg.data
		# self.get_logger().info(f"Command: {command}")
		
		# Simulated motor execution
		if command == "STOP":
			self.get_logger().info("Motor: STOPPED")
		elif command == "MOVE_FORWARD":
			self.get_logger().info("Motor: MOVING FORWARD")

def main(args=None):
	rclpy.init(args=args)
	node = MotorNode()
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