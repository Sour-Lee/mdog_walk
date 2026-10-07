# mdog_walk

ROS 2 package for the Mdog walking and servo-control system.

## Build

Place this directory in a ROS 2 workspace's `src` directory, install the
package dependencies, then build and source the workspace:

```bash
rosdep install --from-paths src --ignore-src -r -y
colcon build --packages-select mdog_walk
source install/setup.bash
```

The serial controller requires access to the configured UART device (default
`/dev/ttyTHS1`). Change `config/servo_config.yaml` for a different device or
servo calibration.

## Run

```bash
ros2 launch mdog_walk servos_control.launch.py
ros2 launch mdog_walk mdog_teleop.launch.py
ros2 launch mdog_walk walk_forward.launch.py
```

`mdog_teleop` expects an interactive Linux terminal. `walk_forward` listens to
`/direction_msg` (`std_msgs/msg/Float64MultiArray`) and publishes servo angles
to `/servos_angle`.

Custom interfaces are `Servo`, `ServoArray`, `ServoAngle`, and `WorldReference`.