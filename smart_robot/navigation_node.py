from smart_robot_interfaces.action import MoveRobot

import rclpy
from rclpy.node import Node
from rclpy.action import ActionServer

class NavigationNode(Node):

    def __init__(self):
      super().__init__('navigation_node')

      self._action_server = ActionServer(self, MoveRobot, 'move_robot', self.execute_callback)
      self.get_logger().info("Action Server Started")

    def execute_callback(self, goal_handle):

      duration = goal_handle.request.duration

      # Reject condition
      if duration <= 0:
          self.get_logger().info("Invalid goal → rejecting")
          goal_handle.abort()
					
          result = MoveRobot.Result()
          result.success = False
					
          return result

      # Accept goal
      self.get_logger().info(f"Goal accepted: {duration}")
      goal_handle.succeed()
			
      result = MoveRobot.Result()
      result.success = True

      return result
      
def main(args=None):
	rclpy.init(args=args)
	node = NavigationNode()
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