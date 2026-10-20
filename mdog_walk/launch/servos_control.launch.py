from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os


def generate_launch_description():
    config = os.path.join(
        get_package_share_directory("mdog_walk"), "config", "servo_config.yaml"
    )
    return LaunchDescription(
        [
            Node(
                package="mdog_walk",
                executable="servos_control",
                name="servos_control",
                output="screen",
                parameters=[config],
            )
        ]
    )