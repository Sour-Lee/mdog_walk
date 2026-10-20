import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node


def generate_launch_description():
    project_launch = os.path.join(
        get_package_share_directory("ncu_mdog"), "launch", "project_sample.launch.py"
    )

    return LaunchDescription(
        [
            # Lidar and base sensor drivers
            IncludeLaunchDescription(PythonLaunchDescriptionSource(project_launch)),
            # Tracking
            Node(
                package="beginner_tutorials",
                executable="laser_tracker",
                name="listener",
                output="screen",
            ),
            # Servo control and walking
            Node(
                package="mdog_walk",
                executable="servos_control",
                name="servos_control",
                output="screen",
            ),
            Node(
                package="mdog_walk",
                executable="walk_forward",
                name="servos_angle_publisher",
                output="screen",
            ),
        ]
    )
