#!/usr/bin/env python

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Imu


class ImuListener(Node):
    def __init__(self):
        super().__init__("imu_listener")
        self.subscription = self.create_subscription(Imu, "/imu/data", self.imu_cb, 10)

    def imu_cb(self, msg):
        self.get_logger().info(f"\norientation : \n{msg.orientation}")
        print("-----------------------------")
        self.get_logger().info(f"\nangular_velocity : \n{msg.angular_velocity}")
        print("-----------------------------")
        self.get_logger().info(f"\nlinear_acceleration : \n{msg.linear_acceleration}")
        with open("data.txt", mode="a") as file:
            file.write(str(msg.orientation) + "\n")
            file.write("-----------------------------\n")


def main(args=None):
    rclpy.init(args=args)
    node = ImuListener()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == "__main__":
    main()
