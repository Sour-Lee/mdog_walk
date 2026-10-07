#!/usr/bin/env python3
import time

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64MultiArray

from mdog_walk.msg import ServoAngle
from foot_pose import (
    foot_raise,
    foot_stand,
    foot_stand_back,
    foot_step,
    foot_step_back,
)


class WalkForward(Node):
    def __init__(self):
        super().__init__("walk_forward")
        self.publisher = self.create_publisher(ServoAngle, "/servos_angle", 10)
        self.subscription = self.create_subscription(
            Float64MultiArray, "/direction_msg", self.direction_callback, 1
        )
        self.first_message = True

    def publish_pose(self, angles):
        message = ServoAngle()
        message.angles = angles
        self.publisher.publish(message)

    def stand(self):
        self.publish_pose(foot_stand * 4)

    def direction_callback(self, message):
        if not message.data:
            self.get_logger().warning("Received an empty direction message")
            return

        x = message.data[0]
        if self.first_message:
            # Let the dog stand up before handling the first direction command.
            time.sleep(0.2)
            self.stand()
            time.sleep(0.2)
            self.first_message = False

        # Keep the original direction range: -x between 1 and 2 triggers a step cycle.
        if -x > 1 and -x < 2 and rclpy.ok():
            self.publish_pose(foot_stand + foot_raise + foot_stand_back + foot_raise)
            time.sleep(0.1)
            self.publish_pose(foot_stand + foot_step_back + foot_stand_back + foot_step)
            time.sleep(0.2)
            self.publish_pose(foot_raise + foot_stand_back + foot_raise + foot_stand)
            time.sleep(0.1)
            self.publish_pose(foot_step + foot_stand_back + foot_step_back + foot_stand)
            time.sleep(0.2)


def main(args=None):
    rclpy.init(args=args)
    node = WalkForward()
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