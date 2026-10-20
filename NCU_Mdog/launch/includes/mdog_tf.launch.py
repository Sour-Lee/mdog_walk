from launch import LaunchDescription
from launch_ros.actions import Node


def static_transform(name, x, y, z, yaw, parent, child):
    return Node(
        package="tf2_ros",
        executable="static_transform_publisher",
        name=name,
        arguments=[
            "--x", str(x), "--y", str(y), "--z", str(z),
            "--yaw", str(yaw), "--pitch", "0", "--roll", "0",
            "--frame-id", parent, "--child-frame-id", child,
        ],
    )


def generate_launch_description():
    return LaunchDescription(
        [
            static_transform("base_footprint2base_link", 0, 0, 0.05, 0, "base_footprint", "base_link"),
            static_transform("base_link2laser_link", -0.03, 0, 0.11, 0, "base_link", "laser_link"),
            static_transform("base_link2imu", 0, 0, 0, 3.1415926, "base_link", "imu_link"),
            static_transform("base_link2camera_link", 0, 0, 0, 0, "base_link", "camera_link"),
            static_transform("map_link2base_footprint_link", 0, 0, 0, 0, "map", "base_footprint"),
        ]
    )
