import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient

from smart_robot_interfaces.action import MoveRobot

class MoveRobotActionClient(Node):

  def __init__(self):
    super().__init__('navigation_action_client')
    self._client = ActionClient(self, MoveRobot, 'move_robot')
    
  def send_goal(self):
    goal_msg = MoveRobot.Goal()
    goal_msg.duration = 10.0 # Duration in seconds

    self.get_logger().info("Sending goal...")
    self._client.wait_for_server()
    
    self._send_goal_future = self._client.send_goal_async(goal_msg)
    self._send_goal_future.add_done_callback(self.goal_response_callback)
    
  def goal_response_callback(self, future):
    self.client_goal_handle = future.result()

    if not self.client_goal_handle.accepted:
      self.get_logger().info("Goal rejected")
      return

    self.get_logger().info("Goal accepted")

    self._get_result_future = self.client_goal_handle.get_result_async()
    self._get_result_future.add_done_callback(self.result_callback)

  def result_callback(self, future):
    result = future.result().result
    self.get_logger().info(f"Final Result: {result.success}")
      
def main(args=None):
	rclpy.init(args=args)
	node = MoveRobotActionClient()
	try:
		node.send_goal()
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
