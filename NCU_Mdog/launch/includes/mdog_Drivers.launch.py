import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource


def generate_launch_description():
    launch_dir = os.path.join(get_package_share_directory("ncu_mdog"), "launch", "includes")
    tf_launch = os.path.join(launch_dir, "mdog_tf.launch.py")
    lidar_launch = os.path.join(launch_dir, "mdog_ydlidar.launch.py")

    return LaunchDescription(
        [
            # TF setting
            IncludeLaunchDescription(PythonLaunchDescriptionSource(tf_launch)),
            # YDLidar
            IncludeLaunchDescription(PythonLaunchDescriptionSource(lidar_launch)),
            # Include mdog_imu.launch.py to start the MPU9250 driver.
            # Include mdog_motor.launch.py to start the walking control nodes.
        ]
    )
