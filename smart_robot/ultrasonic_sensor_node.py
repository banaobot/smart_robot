import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32
import random


class UltrasonicSensorNode(Node):

    def __init__(self):
        super().__init__('ultrasonic_sensor_node')

        # Create publisher
        self.publisher_ = self.create_publisher(Float32, '/distance', 10)

        # Timer to simulate continuous sensor reading
        self.timer = self.create_timer(1.0, self.publish_distance)

        self.get_logger().info("Fake Sensor Node Started")


    def publish_distance(self):
        msg = Float32()

        # Generate fake distance (in meters)
        msg.data = round(random.uniform(0.2, 4.0), 2)

        self.publisher_.publish(msg)

        self.get_logger().info(f"Publishing Distance: {msg.data} m")

def main(args=None):
    rclpy.init(args=args)
    node = UltrasonicSensorNode()
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