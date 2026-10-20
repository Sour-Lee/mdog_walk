import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    calibration_path = get_package_share_directory("ncu_mdog")
    return LaunchDescription(
        [
            Node(
                package="ncu_mdog",
                executable="mpu9250_node",
                name="mpu9250_node",
                output="screen",
                parameters=[
                    {
                        "calibration_file_path": calibration_path,
                        "calibration_file_name": "RTIMULib",
                        "imu_link": "imu_link",
                        "mag_link": "mag_link",
                        "imu_topic_name": "imu",
                        "mag_topic_name": "mag",
                    }
                ],
            )
        ]
    )
