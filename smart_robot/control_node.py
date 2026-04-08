import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from std_srvs.srv import SetBool


class ControlNode(Node):
    
  def __init__(self):
    super().__init__('control_node')

    # Publisher to broadcast robot state
    self.publisher_ = self.create_publisher(String, '/robot_state', 10)

    # Service server
    self.srv = self.create_service(SetBool, 'robot_control', self.control_callback)

    self.get_logger().info("Control Node Started")

  def control_callback(self, request, response):

    msg = String()

    if request.data:
      msg.data = "START"
      response.message = "Robot Started"
    else:
      msg.data = "STOP"
      response.message = "Robot Stopped"
    self.publisher_.publish(msg)
    response.success = True
    self.get_logger().info(f"Service: {response.message}")
    return response

def main(args=None):
	rclpy.init(args=args)
	node = ControlNode()
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