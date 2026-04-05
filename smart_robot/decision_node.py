import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32, String


class DecisionNode(Node):

  def __init__(self):
    super().__init__('decision_node')
    # Subscribe to sensor
    self.subscription = self.create_subscription(Float32, '/distance', self.distance_callback, 10)

    # Publish command
    self.publisher_ = self.create_publisher(String, '/cmd_vel', 10)
    self.get_logger().info("Decision Node Started")

  def distance_callback(self, msg):
    distance = msg.data
    cmd = String()
    if distance < 1.0:
      cmd.data = "STOP"
    else:
      cmd.data = "MOVE_FORWARD"
    
    self.publisher_.publish(cmd)
    self.get_logger().info(f"[Decision] Distance: {distance} -> {cmd.data}")

def main(args=None):
	rclpy.init(args=args)
	node = DecisionNode()
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