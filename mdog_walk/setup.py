from glob import glob
import os

from setuptools import setup

package_name = "mdog_walk"

setup(
    name=package_name,
    version="0.1.0",
    packages=[package_name],
    data_files=[
        ("share/ament_index/resource_index/packages", [f"resource/{package_name}"]),
        (os.path.join("share", package_name), ["package.xml"]),
        (os.path.join("share", package_name, "launch"), glob("launch/*.launch.py")),
        (os.path.join("share", package_name, "config"), glob("config/*")),
    ],
    install_requires=["setuptools", "numpy", "pyserial"],
    zip_safe=True,
    maintainer="mdog",
    maintainer_email="mdog@todo.todo",
    description="ROS 2 Python nodes for the Mdog walking and servo-control system.",
    license="TODO",
    entry_points={
        "console_scripts": [
            "mdog_teleop = mdog_walk.mdog_teleop:main",
            "servos_control = mdog_walk.servos_control:main",
            "walk_forward = mdog_walk.walk_forward:main",
        ],
    },
)