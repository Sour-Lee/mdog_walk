from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
  return LaunchDescription(
    [
      Node(
        package="ncu_mdog",
        executable="ydlidar_node",
        name="ydlidar_node",
        output="screen",
        parameters=[
          {
            "port": "/dev/ydlidar",
            "baudrate": 128000,
            "frame_id": "laser_link",
            "resolution_fixed": True,
            "auto_reconnect": True,
            "reversion": False,
            "angle_min": -180.0,
            "angle_max": 180.0,
            "range_min": 0.1,
            "range_max": 12.0,
            "ignore_array": "",
            "frequency": 8.0,
            "samp_rate": 5,
          }
        ],
      )
    ]
  )
