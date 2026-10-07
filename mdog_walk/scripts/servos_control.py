#!/usr/bin/env python3
import numpy as np
import rclpy
from rclpy.node import Node

from mdog_walk.msg import Servo, ServoAngle, ServoArray
from uart_servo_controller import UART_Servo_Controller


# Servo angle 1.0 means that the servo should not move.
class ServosControl(Node):
    def __init__(self):
        super().__init__("servos_control")

        # Parameters are loaded from config/servo_config.yaml by the launch file.
        self.declare_parameter("com_port", "/dev/ttyTHS1")
        self.declare_parameter("center", [500.0] * 12)
        self.declare_parameter("range", [750.0] * 12)
        self.declare_parameter("direction", [1, 1, 1, 1, 1, -1, -1, -1, 1, -1, -1, -1])

        self.com_port = self.get_parameter("com_port").value
        self.servos_center = np.asarray(self.get_parameter("center").value, dtype=float)
        self.servos_range = np.asarray(self.get_parameter("range").value, dtype=float)
        self.servos_direction = np.asarray(self.get_parameter("direction").value, dtype=float)

        # The controller has 12 servos; reject incomplete calibration values.
        if any(values.size != 12 for values in (self.servos_center, self.servos_range, self.servos_direction)):
            raise ValueError("center, range, and direction parameters must each contain 12 values")

        # Convert the requested angle in degrees to the servo's 0-1000 position units.
        self.servo_scale = self.servos_range / 180.0
        self.uart_ctrl = UART_Servo_Controller(self.com_port)
        self.publisher = self.create_publisher(ServoArray, "/servos_absolute", 1)
        self.subscription = self.create_subscription(
            ServoAngle, "/servos_angle", self.servos_angle_callback, 10
        )

    def servos_angle_callback(self, data):
        if len(data.angles) != 12:
            self.get_logger().error("Received servo angle message must contain 12 angles")
            return

        servo_array = ServoArray()
        servo_to_move = []
        positions = []
        for index, angle in enumerate(data.angles):
            servo = Servo()
            servo.servo = index + 1
            if angle == 1.0:
                servo.value = 1.0
            else:
                # Apply each servo's center point, range, and rotation direction.
                position = int(round(angle * self.servo_scale[index] * self.servos_direction[index]
                                     + self.servos_center[index]))
                servo.value = float(position)
                servo_to_move.append(index + 1)
                positions.append(position)
            servo_array.servos.append(servo)

        self.publisher.publish(servo_array)
        if servo_to_move:
            self.uart_ctrl.cmd_servo_move(servo_to_move, positions, 100)

        # Warn below 5.0 V and stop the node below the 4.1 V safety threshold.
        voltage = self.uart_ctrl.cmd_get_battery_voltage()
        if voltage is None:
            self.get_logger().warning("Could not read servo battery voltage")
        elif voltage >= 5.0:
            return
        elif voltage >= 4.1:
            self.get_logger().warning(f"Servo voltage is low: {voltage:.2f} V")
        else:
            self.get_logger().error("Servo voltage is below 4.1 V; shutting down")
            rclpy.try_shutdown()

    def unload_servos(self):
        if self.uart_ctrl is not None:
            # Release all servos when the node shuts down.
            self.get_logger().info("Shutting down; unloading all servos")
            self.uart_ctrl.cmd_mult_servo_unload(list(range(1, 13)))


def main(args=None):
    rclpy.init(args=args)
    node = None
    try:
        node = ServosControl()
        rclpy.spin(node)
    except (OSError, ValueError) as error:
        if node is not None:
            node.get_logger().error(str(error))
        else:
            print(error)
    finally:
        if node is not None:
            try:
                node.unload_servos()
            except OSError as error:
                node.get_logger().error(f"Failed to unload servos: {error}")
            node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == "__main__":
    main()