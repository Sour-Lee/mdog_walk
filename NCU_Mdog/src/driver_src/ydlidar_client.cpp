/*
 *  YDLIDAR SYSTEM
 *  YDLIDAR ROS Node Client 
 *
 *  Copyright 2015 - 2018 EAI TEAM
 *  http://www.ydlidar.com
 * 
 */

#include "rclcpp/rclcpp.hpp"
#include "sensor_msgs/msg/laser_scan.hpp"
#include <cmath>

#define RAD2DEG(x) ((x)*180./M_PI)

void scanCallback(const sensor_msgs::msg::LaserScan::ConstSharedPtr scan)
{
    int count = scan->scan_time / scan->time_increment;
    printf("[YDLIDAR INFO]: I heard a laser scan %s[%d]:\n", scan->header.frame_id.c_str(), count);
    printf("[YDLIDAR INFO]: angle_range : [%f, %f]\n", RAD2DEG(scan->angle_min), RAD2DEG(scan->angle_max));
  
    for(int i = 0; i < count; i++) {
        float degree = RAD2DEG(scan->angle_min + scan->angle_increment * i);
	if(degree > -5 && degree< 5)
        printf("[YDLIDAR INFO]: angle-distance : [%f, %f, %i]\n", degree, scan->ranges[i], i);
    }
}

int main(int argc, char **argv)
{
    rclcpp::init(argc, argv);
    auto node = std::make_shared<rclcpp::Node>("ydlidar_client");
    auto sub = node->create_subscription<sensor_msgs::msg::LaserScan>("/scan", 1000, scanCallback);
    rclcpp::spin(node);
    rclcpp::shutdown();

    return 0;
}
