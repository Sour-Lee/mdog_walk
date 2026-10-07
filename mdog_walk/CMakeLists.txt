cmake_minimum_required(VERSION 3.8)
project(mdog_walk)

find_package(ament_cmake REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(rosidl_default_generators REQUIRED)

rosidl_generate_interfaces(${PROJECT_NAME}
  "msg/Servo.msg"
  "msg/ServoArray.msg"
  "msg/ServoAngle.msg"
  "msg/WorldReference.msg"
  DEPENDENCIES geometry_msgs
)

install(PROGRAMS
  scripts/mdog_teleop.py
  scripts/servos_control.py
  scripts/walk_forward.py
  DESTINATION lib/${PROJECT_NAME}
)

install(FILES
  scripts/foot_pose.py
  scripts/uart_servo_controller.py
  DESTINATION lib/${PROJECT_NAME}
)

install(DIRECTORY launch config
  DESTINATION share/${PROJECT_NAME}
)

ament_export_dependencies(rosidl_default_runtime)
ament_package()