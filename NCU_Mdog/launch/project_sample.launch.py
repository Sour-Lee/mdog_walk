import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
  package_share = get_package_share_directory("ncu_mdog")
  drivers_launch = os.path.join(package_share, "launch", "includes", "mdog_Drivers.launch.py")

  # rviz can be launched separately with the saved configuration.
  return LaunchDescription(
    [
      DeclareLaunchArgument("launch_realsense", default_value="false"),
      IncludeLaunchDescription(PythonLaunchDescriptionSource(drivers_launch)),
      Node(
        package="ncu_mdog",
        executable="main",
        name="main",
        output="screen",
      ),
      IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
          PathJoinSubstitution(
            [FindPackageShare("realsense2_camera"), "launch", "rs_launch.py"]
          )
        ),
        condition=IfCondition(LaunchConfiguration("launch_realsense")),
      ),
      # The optional RGBD sample can be launched after installing its ROS 2 package.
    ]
  )
