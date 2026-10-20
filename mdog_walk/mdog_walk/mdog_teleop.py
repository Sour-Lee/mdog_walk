#!/usr/bin/env python3
import select
import sys
import termios
import time
import tty

import rclpy
from rclpy.node import Node

from mdog_walk_msg.msg import ServoAngle
from .foot_pose import (
    foot_raise,
    foot_raise_back,
    foot_stand,
    foot_stand_back,
    foot_stay,
    foot_step,
    foot_step_back,
    foot_right_l,
    foot_right_l_back,
    foot_right_r,
    foot_right_r_back,
)


msg = """
Control Mdog
---------------------------
Moving around:
    w
   a    s    d


W : walk forward
A : walk left
D : walk right

S, space key : stop and stand

CTRL-C or Q to quit
"""


class MdogTeleop(Node):
    def __init__(self):
        super().__init__("mdog_teleop")
        self.publisher = self.create_publisher(ServoAngle, "/servos_angle", 10)

    def publish_pose(self, angles):
        message = ServoAngle()
        message.angles = angles
        self.publisher.publish(message)

    def first_stand(self):
        self.publish_pose(foot_stay + foot_stand + foot_stand + foot_stay)
        time.sleep(0.5)

        self.publish_pose(foot_stand + foot_stay + foot_stay + foot_stand)
        time.sleep(0.5)

    def stand(self):
        self.publish_pose(foot_stand + foot_stand + foot_stand + foot_stand)
        time.sleep(0.5)

    def walk_forward(self):
        self.publish_pose(foot_raise + foot_stand_back + foot_raise + foot_stand)
        time.sleep(0.1)

        self.publish_pose(foot_step + foot_stand_back + foot_step_back + foot_stand)
        time.sleep(0.2)

        self.publish_pose(foot_stand + foot_raise + foot_stand_back + foot_raise)
        time.sleep(0.1)

        self.publish_pose(foot_stand + foot_step_back + foot_stand_back + foot_step)
        time.sleep(0.2)

    def walk_backward(self):
        pass

    def walk_left(self):
        self.publish_pose(foot_stand + foot_raise_back + foot_stand_back + foot_raise)
        time.sleep(0.1)

        self.publish_pose(foot_right_r + foot_raise_back + foot_right_l_back + foot_raise)
        time.sleep(0.1)

        self.publish_pose(foot_stand + foot_step_back + foot_stand_back + foot_step)
        time.sleep(0.1)

        self.publish_pose(foot_raise + foot_stand_back + foot_raise_back + foot_stand)
        time.sleep(0.1)

        self.publish_pose(foot_step + foot_stand_back + foot_step_back + foot_stand)
        time.sleep(0.1)

    def walk_right(self):
        self.publish_pose(foot_raise + foot_stand_back + foot_raise_back + foot_stand)
        time.sleep(0.1)

        self.publish_pose(foot_raise + foot_right_r_back + foot_raise_back + foot_right_l)
        time.sleep(0.1)

        self.publish_pose(foot_step + foot_stand_back + foot_step_back + foot_stand)
        time.sleep(0.1)

        self.publish_pose(foot_stand + foot_raise_back + foot_stand_back + foot_raise)
        time.sleep(0.1)

        self.publish_pose(foot_stand + foot_step_back + foot_stand_back + foot_step)
        time.sleep(0.1)


def get_key():
    tty.setraw(sys.stdin.fileno())
    readable, _, _ = select.select([sys.stdin], [], [], 0.1)
    return sys.stdin.read(1) if readable else ""


def main(args=None):
    if not sys.stdin.isatty():
        raise RuntimeError("mdog_teleop requires an interactive terminal")

    old_settings = termios.tcgetattr(sys.stdin)
    new_settings = termios.tcgetattr(sys.stdin)
    new_settings[3] &= ~termios.ECHO
    node = None
    rclpy.init(args=args)
    try:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, new_settings)
        node = MdogTeleop()
        node.stand()
        print(msg)
        while rclpy.ok():
            key = get_key()
            if key == "w":
                node.walk_forward()
            elif key == "x":
                node.walk_backward()
            elif key == "a":
                node.walk_left()
            elif key == "d":
                node.walk_right()
            elif key in (" ", "s"):
                node.stand()
            elif key in ("\x03", "q"):
                break
    except KeyboardInterrupt:
        pass
    finally:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
        if node is not None:
            node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == "__main__":
    main()