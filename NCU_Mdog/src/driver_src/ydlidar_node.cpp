/*
 *  YDLIDAR SYSTEM
 *  YDLIDAR ROS Node Client 
 *
 *  Copyright 2015 - 2018 EAI TEAM
 *  http://www.ydlidar.com
 * 
 */

#include <cstdlib>
#include <sstream>

#include "rclcpp/rclcpp.hpp"
#include "sensor_msgs/msg/laser_scan.hpp"
#include "CYdLidar.h"
#include <vector>
#include <iostream>
#include <string>
#include <signal.h>

using namespace ydlidar;

#define ROSVerision "2.0.0"


std::vector<float> split(const std::string &s, char delim) {
    std::vector<float> elems;
    std::stringstream ss(s);
    std::string number;
    while(std::getline(ss, number, delim)) {
        elems.push_back(atof(number.c_str()));
    }
    return elems;
}


int main(int argc, char * argv[]) {

    printf("__   ______  _     ___ ____    _    ____  \n");
    printf("\\ \\ / /  _ \\| |   |_ _|  _ \\  / \\  |  _ \\ \n");
    printf(" \\ V /| | | | |    | || | | |/ _ \\ | |_) | \n");
    printf("  | | | |_| | |___ | || |_| / ___ \\|  _ <  \n");
    printf("  |_| |____/|_____|___|____/_/   \\_\\_| \\_\\ \n");
    printf("\n");
    fflush(stdout);
    rclcpp::init(argc, argv);
    auto node = std::make_shared<rclcpp::Node>("ydlidar_node");

    std::string port;
    int baudrate=115200;
    std::string model;
    std::string frame_id;
    bool intensities,low_exposure,reversion, resolution_fixed;
    bool auto_reconnect;
    double angle_max,angle_min;
    int samp_rate;
    std::string list;
    std::vector<float> ignore_array;  
    double max_range, min_range;
    double _frequency;

    auto scan_pub = node->create_publisher<sensor_msgs::msg::LaserScan>("scan", 1000);
    port = node->declare_parameter<std::string>("port", "/dev/ydlidar");
    baudrate = node->declare_parameter<int>("baudrate", 115200);
    frame_id = node->declare_parameter<std::string>("frame_id", "laser_frame");
    resolution_fixed = node->declare_parameter<bool>("resolution_fixed", true);
    intensities = node->declare_parameter<bool>("intensity", false);
    low_exposure = node->declare_parameter<bool>("low_exposure", false);
    auto_reconnect = node->declare_parameter<bool>("auto_reconnect", true);
    reversion = node->declare_parameter<bool>("reversion", false);
    angle_max = node->declare_parameter<double>("angle_max", 180.0);
    angle_min = node->declare_parameter<double>("angle_min", -180.0);
    samp_rate = node->declare_parameter<int>("samp_rate", 4);
    max_range = node->declare_parameter<double>("range_max", 16.0);
    min_range = node->declare_parameter<double>("range_min", 0.08);
    _frequency = node->declare_parameter<double>("frequency", 7.0);
    list = node->declare_parameter<std::string>("ignore_array", "");

    ignore_array = split(list ,',');
    if(ignore_array.size()%2){
        RCLCPP_ERROR(node->get_logger(), "ignore array is odd need be even");
    }

    for(uint16_t i =0 ; i < ignore_array.size();i++){
        if(ignore_array[i] < -180 || ignore_array[i] > 180){
            RCLCPP_ERROR(node->get_logger(), "ignore array should be between -180 and 180");
        }
    }

    CYdLidar laser;
    if(_frequency<5){
       _frequency = 7.0; 
    }
    if(_frequency>12){
        _frequency = 12;
    }
    if(angle_max < angle_min){
        double temp = angle_max;
        angle_max = angle_min;
        angle_min = temp;
    }

    laser.setSerialPort(port);
    laser.setSerialBaudrate(baudrate);
    laser.setIntensities(intensities);
    laser.setMaxRange(max_range);
    laser.setMinRange(min_range);
    laser.setMaxAngle(angle_max);
    laser.setMinAngle(angle_min);
    laser.setReversion(reversion);
    laser.setFixedResolution(resolution_fixed);
    laser.setAutoReconnect(auto_reconnect);
    laser.setExposure(low_exposure);
    laser.setScanFrequency(_frequency);
    laser.setSampleRate(samp_rate);
    laser.setReversion(reversion);
    laser.setIgnoreArray(ignore_array);
    laser.initialize();

    rclcpp::Rate rate(30.0);

    while (rclcpp::ok()) {
        bool hardError;
        LaserScan scan;//原始激光数据
        if(laser.doProcessSimple(scan, hardError )){
            sensor_msgs::msg::LaserScan scan_msg;
            scan_msg.header.stamp = rclcpp::Time(static_cast<int64_t>(scan.system_time_stamp)).to_msg();
            scan_msg.header.frame_id = frame_id;
            scan_msg.angle_min = scan.config.min_angle;
            scan_msg.angle_max = scan.config.max_angle;
            scan_msg.angle_increment = scan.config.ang_increment;
            scan_msg.scan_time = 1/_frequency;//scan.config.scan_time;
            scan_msg.time_increment = 1/((float)samp_rate*1000); //scan.config.time_increment;
            scan_msg.range_min = scan.config.min_range;
            scan_msg.range_max = scan.config.max_range;
            
            scan_msg.ranges = scan.ranges;
            scan_msg.intensities =  scan.intensities;
            scan_pub->publish(scan_msg);
        }  
        rate.sleep();
        rclcpp::spin_some(node);
    }

    laser.turnOff();
    printf("[YDLIDAR INFO] Now YDLIDAR is stopping .......\n");
    laser.disconnecting();
    rclcpp::shutdown();
    return 0;
}
