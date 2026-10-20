cmake_minimum_required(VERSION 3.8)
project(ncu_mdog)

# Compile the ROS 2 nodes and the bundled YDLIDAR SDK with C++14.
if(NOT CMAKE_CXX_STANDARD)
  set(CMAKE_CXX_STANDARD 14)
endif()

find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(sensor_msgs REQUIRED)
find_package(std_msgs REQUIRED)
find_package(visualization_msgs REQUIRED)
find_package(Threads REQUIRED)

# RTIMULib is installed separately and is required by the MPU9250 driver.
find_library(RTIMULIB_LIBRARY NAMES RTIMULib)
if(NOT RTIMULIB_LIBRARY)
  message(FATAL_ERROR "RTIMULib was not found. Install RTIMULib before building ncu_mdog.")
endif()

# Build the bundled Unix serial and timer implementation for the YDLIDAR SDK.
file(GLOB YDLIDAR_SDK_SOURCES
  "${PROJECT_SOURCE_DIR}/sdk/src/impl/unix/*.cpp"
  "${PROJECT_SOURCE_DIR}/sdk/src/*.cpp"
  "${PROJECT_SOURCE_DIR}/sdk/src/*.c"
)

add_library(ncu_mdog_ydlidar_sdk ${YDLIDAR_SDK_SOURCES})
target_include_directories(ncu_mdog_ydlidar_sdk PUBLIC
  ${PROJECT_SOURCE_DIR}/sdk/include
  ${PROJECT_SOURCE_DIR}/sdk/src
)
target_link_libraries(ncu_mdog_ydlidar_sdk Threads::Threads rt)

# Build the hardware drivers and their sample subscriber nodes.
add_executable(ydlidar_node src/driver_src/ydlidar_node.cpp)
target_include_directories(ydlidar_node PRIVATE ${PROJECT_SOURCE_DIR}/sdk/include)
target_link_libraries(ydlidar_node ncu_mdog_ydlidar_sdk)
ament_target_dependencies(ydlidar_node rclcpp sensor_msgs)

add_executable(ydlidar_client src/driver_src/ydlidar_client.cpp)
ament_target_dependencies(ydlidar_client rclcpp sensor_msgs)

add_executable(main src/main.cpp)
ament_target_dependencies(main rclcpp sensor_msgs std_msgs visualization_msgs)

add_executable(mpu9250_node src/driver_src/mpu9250_node.cpp)
target_link_libraries(mpu9250_node ${RTIMULIB_LIBRARY})
ament_target_dependencies(mpu9250_node rclcpp sensor_msgs)

add_executable(mpu9250_client src/driver_src/mpu9250_client.cpp)
ament_target_dependencies(mpu9250_client rclcpp sensor_msgs)

# Install node executables for ros2 run and the Python launch descriptions.
install(TARGETS
  ydlidar_node
  ydlidar_client
  main
  mpu9250_node
  mpu9250_client
  DESTINATION lib/${PROJECT_NAME}
)

# Install launch files, RViz settings, SDK sources, and hardware setup scripts.
install(PROGRAMS script/main.py DESTINATION lib/${PROJECT_NAME})
install(DIRECTORY launch rviz startup sdk DESTINATION share/${PROJECT_NAME})
install(FILES RTIMULib.ini DESTINATION share/${PROJECT_NAME})

ament_package()
