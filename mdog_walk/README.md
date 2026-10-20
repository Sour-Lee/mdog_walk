# mdog_walk

ROS 2 Python nodes for the Mdog walking and servo-control system. Custom
interfaces are provided by the sibling `mdog_walk_interfaces` package.

## Build

Place both packages in the `src` directory of a ROS 2 workspace, install their
dependencies, then build and source the workspace:

```bash
rosdep install --from-paths src --ignore-src -r -y
colcon build --packages-up-to mdog_walk
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
