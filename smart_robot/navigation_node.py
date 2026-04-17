import rclpy
from rclpy.node import Node
from rclpy.action import ActionServer

from smart_robot_interfaces.action import MoveRobot
import time

class NavigationNode(Node):

  def __init__(self):
    super().__init__('navigation_node')

    self._action_server = ActionServer(self, MoveRobot, 'move_robot', self.execute_callback)
    self.get_logger().info("Action Server Started")

  def execute_callback(self, goal_handle):

    duration = goal_handle.request.duration
      
    # Abort condition
    if duration <= 0:
      self.get_logger().info("Invalid goal: Duration must be positive. Aborting...")
      goal_handle.abort()
          
      result = MoveRobot.Result()
      result.success = False
          
      return result

    # Execute goal
    self.get_logger().info(f"Executing Goal: {duration}")
    feedback_msg = MoveRobot.Feedback()
    start_time = time.time()
    
    while time.time() - start_time < duration:
      
      feedback_msg.time_elapsed = time.time() - start_time
      goal_handle.publish_feedback(feedback_msg)
    
      time.sleep(1)  # Sleep for 1 second
      
    self.get_logger().info("Goal execution completed successfully.")
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