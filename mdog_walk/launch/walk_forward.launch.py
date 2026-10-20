from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os


def generate_launch_description():
    package_share = get_package_share_directory("mdog_walk")
    servo_launch = os.path.join(package_share, "launch", "servos_control.launch.py")
    return LaunchDescription(
        [
            IncludeLaunchDescription(PythonLaunchDescriptionSource(servo_launch)),
            Node(
                package="mdog_walk",
                executable="walk_forward",
                name="walk_forward",
                output="screen",
            ),
        ]
    )