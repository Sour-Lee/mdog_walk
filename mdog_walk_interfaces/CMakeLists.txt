cmake_minimum_required(VERSION 3.8)
project(mdog_walk_interfaces)

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

ament_export_dependencies(rosidl_default_runtime)
ament_package()
