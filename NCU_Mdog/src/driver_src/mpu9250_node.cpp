#include <memory>
#include <string>

#include <RTIMULib.h>
#include <rclcpp/rclcpp.hpp>
#include <sensor_msgs/msg/imu.hpp>
#include <sensor_msgs/msg/magnetic_field.hpp>

int main(int argc, char **argv) {
    rclcpp::init(argc, argv);
    auto node = std::make_shared<rclcpp::Node>("mpu9250_node");
    RCLCPP_INFO(node->get_logger(), "Imu driver is now running");

    node->declare_parameter<double>("mag_cov", 0.5);
    node->declare_parameter<double>("ori_cov", 0.0025);
    node->declare_parameter<double>("vel_cov", 0.02);
    node->declare_parameter<double>("acc_cov", 0.04);
    node->declare_parameter<int>("imu_i2c", 0x68);
    node->declare_parameter<std::string>("imu_link", "imu_link");
    node->declare_parameter<std::string>("mag_link", "mag_link");

    const auto imu_topic_name = node->declare_parameter<std::string>("imu_topic_name", "imu/data");
    const auto mag_topic_name = node->declare_parameter<std::string>("mag_topic_name", "mag/data");
    const auto calibration_file_path = node->declare_parameter<std::string>("calibration_file_path", "");
    const auto calibration_file_name = node->declare_parameter<std::string>("calibration_file_name", "RTIMULib");
    const auto imu_link = node->get_parameter("imu_link").as_string();
    const auto mag_link = node->get_parameter("mag_link").as_string();

    if (calibration_file_path.empty()) {
        RCLCPP_ERROR(node->get_logger(), "The calibration_file_path parameter must be set to use a calibration file.");
        rclcpp::shutdown();
        return -1;
    }

    auto imu_pub = node->create_publisher<sensor_msgs::msg::Imu>(imu_topic_name, 1000);
    auto mag_pub = node->create_publisher<sensor_msgs::msg::MagneticField>(mag_topic_name, 1000);

    // Load the RTIMULib.ini config file
    RTIMUSettings *settings = new RTIMUSettings(calibration_file_path.c_str(), calibration_file_name.c_str());
    RTIMU *imu = RTIMU::createIMU(settings);

    if ((imu == nullptr) || (imu->IMUType() == RTIMU_TYPE_NULL)) {
        RCLCPP_ERROR(node->get_logger(), "No Imu found");
        rclcpp::shutdown();
        return -1;
    }
    RCLCPP_INFO(node->get_logger(), "Found Imu!");

    // Initialise the imu object
    imu->IMUInit();

    // Set the Fusion coefficient
    imu->setSlerpPower(0.02);
    // Enable the sensors
    imu->setGyroEnable(true);
    imu->setAccelEnable(true);
    imu->setCompassEnable(true);

    const int poll_interval = imu->IMUGetPollInterval();
    const double publish_frequency = poll_interval > 0 ? 1000.0 / poll_interval : 1.0;
    rclcpp::Rate loop_rate(publish_frequency);
    node->declare_parameter<double>("pub_freq", publish_frequency);
    RCLCPP_INFO(node->get_logger(), "Get in while loop");

    while (rclcpp::ok()) {
        sensor_msgs::msg::Imu imu_msg;
        sensor_msgs::msg::MagneticField mag_msg;

        if (imu->IMURead()) {
            RTIMU_DATA imu_data = imu->getIMUData();
            mag_msg.header.stamp = node->now().to_msg();
            mag_msg.header.frame_id = mag_link;
            mag_msg.magnetic_field.z = imu_data.compass.x();
            mag_msg.magnetic_field.y = imu_data.compass.y();
            mag_msg.magnetic_field.x = imu_data.compass.z();
            imu_msg.header.stamp = node->now().to_msg();
            imu_msg.header.frame_id = imu_link;
            imu_msg.orientation.x = imu_data.fusionQPose.x();
            imu_msg.orientation.y = imu_data.fusionQPose.y();
            imu_msg.orientation.z = imu_data.fusionQPose.z();
            imu_msg.orientation.w = imu_data.fusionQPose.scalar();
            imu_msg.angular_velocity.x = imu_data.gyro.x();
            imu_msg.angular_velocity.y = imu_data.gyro.y();
            imu_msg.angular_velocity.z = imu_data.gyro.z();
            imu_msg.linear_acceleration.x = imu_data.accel.x() * 9.80665;
            imu_msg.linear_acceleration.y = imu_data.accel.y() * 9.80665;
            imu_msg.linear_acceleration.z = imu_data.accel.z() * 9.80665;

            imu_pub->publish(imu_msg);
            mag_pub->publish(mag_msg);
        }

        rclcpp::spin_some(node);
        loop_rate.sleep();
    }

    delete imu;
    delete settings;
    rclcpp::shutdown();
    return 0;
}
