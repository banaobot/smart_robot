from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    
    # Launch Arguments
    threshold_arg = DeclareLaunchArgument(
        'threshold',
        default_value='1.0',
        description='Obstacle distance threshold'
    )

    # Launch Configurations
    threshold_config = LaunchConfiguration('threshold')

    # Nodes
    ultrasonic_node = Node(
        package='smart_robot',
        executable='ultrasonic_node',
        name='ultrasonic_sensor_node',
    )

    decision_node = Node(
        package='smart_robot',
        executable='decision_node',
        name='decision_node',
        parameters=[{
            'distance_threshold': threshold_config
        }]
    )

    motor_node = Node(
        package='smart_robot',
        executable='motor_node',
        name='motor_node'
    )

    return LaunchDescription([
        threshold_arg,
        ultrasonic_node,
        decision_node,
        motor_node
    ])