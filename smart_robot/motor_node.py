import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class MotorNode(Node):

	def __init__(self):
		super().__init__('motor_node')

		# Internal state
		self.current_command = "STOP"
		self.robot_active = False

		# Subscribe to command
		self.cmd_sub = self.create_subscription(String, '/cmd_vel', self.cmd_callback, 10)

		# Subscribe to robot state
		self.state_sub = self.create_subscription(String, '/robot_state', self.state_callback, 10)

		self.get_logger().info("Motor Node Started")

	def cmd_callback(self, msg):
		self.current_command = msg.data
		self.get_logger().info("Command Callback: " + self.current_command)

		self.execute()

	def state_callback(self, msg):
		if msg.data == "START":
			self.robot_active = True
		elif msg.data == "STOP":
			self.robot_active = False

		self.execute()

	def execute(self):

		# Final decision logic
		if not self.robot_active:
			self.get_logger().info("Robot Disabled)")
			return

		if self.current_command == "STOP":
			self.get_logger().info("Motor: STOPPED")
		elif self.current_command == "MOVE_FORWARD":
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