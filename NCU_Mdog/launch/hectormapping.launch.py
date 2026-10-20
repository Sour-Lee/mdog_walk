from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
  return LaunchDescription(
    [
      Node(
        package="hector_mapping",
        executable="hector_mapping",
        name="hector_height_mapping",
        output="screen",
        parameters=[
          {
            "scan_topic": "scan",
            "base_frame": "base_link",
            "odom_frame": "base_link",
            "output_timing": False,
            "advertise_map_service": True,
            "use_tf_scan_transformation": True,
            "use_tf_pose_start_estimate": False,
            "pub_map_odom_transform": True,
            "map_with_known_poses": False,
            "map_pub_period": 0.5,
            "update_factor_free": 0.45,
            "map_update_distance_thresh": 0.02,
            "map_update_angle_thresh": 0.1,
            "map_resolution": 0.05,
            "map_size": 1024,
            "map_start_x": 0.5,
            "map_start_y": 0.5,
          }
        ],
      )
    ]
  )
