from glob import glob
import os

from setuptools import setup

package_name = "beginner_tutorials"

setup(
    name=package_name,
    version="0.0.0",
    packages=[package_name],
    data_files=[
        ("share/ament_index/resource_index/packages", [f"resource/{package_name}"]),
        (os.path.join("share", package_name), ["package.xml"]),
        (os.path.join("share", package_name, "launch"), glob("launch/*.launch.py")),
        (os.path.join("share", package_name, "rviz"), glob("rviz/*")),
        (os.path.join("share", package_name, "urdf"), glob("urdf/*")),
    ],
    install_requires=["setuptools", "numpy"],
    zip_safe=True,
    maintainer="david",
    maintainer_email="david@todo.todo",
    description="ROS 2 Python tutorial nodes for IMU and laser data.",
    license="TODO",
    entry_points={
        "console_scripts": [
            "imu_listener = beginner_tutorials.imu:main",
            "laser_listener = beginner_tutorials.laser:main",
            "laser_tracker = beginner_tutorials.main:main",
            "rviz_test = beginner_tutorials.rviz_test:main",
        ],
    },
)