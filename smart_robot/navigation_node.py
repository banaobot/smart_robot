import rclpy
from rclpy.node import Node
from rclpy.action import ActionServer, CancelResponse, GoalResponse

from rclpy.executors import MultiThreadedExecutor

from smart_robot_interfaces.action import MoveRobot
import time

class NavigationNode(Node):

  def __init__(self):
    super().__init__('navigation_node')

    self._action_server = ActionServer(self, MoveRobot, 'move_robot',execute_callback=self.execute_callback, cancel_callback=self.cancel_callback, goal_callback=self.goal_callback)
    
    self.get_logger().info("Action Server Started")

  def goal_callback(self, goal_request):
    duration = goal_request.duration
    if duration <= 0:
      self.get_logger().info(f"Received invalid goal: {duration}. Rejecting...")
      return GoalResponse.REJECT
    
    self.get_logger().info(f"Received new goal: {duration}")
    return GoalResponse.ACCEPT

  def cancel_callback(self, goal_handle):
    self.get_logger().info(f"Received cancel request: {goal_handle.request.duration}")
    return CancelResponse.ACCEPT

  def execute_callback(self, goal_handle):

    duration = goal_handle.request.duration
      
    # We can Abort condition here if needed
    
    # Execute goal
    self.get_logger().info(f"Executing Goal: {duration}")
    feedback_msg = MoveRobot.Feedback()
    start_time = time.time()
    
    while time.time() - start_time < duration:

      # Check if cancel requested
      if goal_handle.is_cancel_requested:
        goal_handle.canceled()
        self.get_logger().info("Goal canceled")
        
        result = MoveRobot.Result()
        result.success = False
        return result
      
      feedback_msg.time_elapsed = time.time() - start_time
      goal_handle.publish_feedback(feedback_msg)
    
      time.sleep(0.1)  # Sleep for 0.1 second
      
    self.get_logger().info("Goal execution completed successfully.")
    goal_handle.succeed()
      
    result = MoveRobot.Result()
    result.success = True

    return result
      
def main(args=None):
  rclpy.init(args=args)
  node = NavigationNode()
  try:
    executor = MultiThreadedExecutor()
    executor.add_node(node)
    executor.spin()
    
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