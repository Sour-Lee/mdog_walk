#include <rclcpp/rclcpp.hpp>
#include <sensor_msgs/msg/imu.hpp>

void ImuCallback( const sensor_msgs::msg::Imu::ConstSharedPtr imu_msg ) {
    RCLCPP_INFO( rclcpp::get_logger("imu_listener"), "Sucess subscribe to imu_publisher" );
    RCLCPP_INFO( rclcpp::get_logger("imu_listener"), "Imu Orientation x: [%f], y: [%f], z: [%f], w: [%f]", imu_msg->orientation.x, imu_msg->orientation.y, imu_msg->orientation.z, imu_msg->orientation.w );
    RCLCPP_INFO( rclcpp::get_logger("imu_listener"), "IMU Angilar velocity x: [%f], y[%f], z[%f]", imu_msg->angular_velocity.x, imu_msg->angular_velocity.y, imu_msg->angular_velocity.z );
    RCLCPP_INFO( rclcpp::get_logger("imu_listener"), "IMU Linear acceleration x: [%f], y[%f], z[%f]\n", imu_msg->linear_acceleration.x, imu_msg->linear_acceleration.y, imu_msg->linear_acceleration.z );
}

int main( int argc, char **argv ) {

    rclcpp::init( argc, argv );
    auto node = std::make_shared<rclcpp::Node>("imu_listener");
    RCLCPP_INFO(node->get_logger(), "Imu Subscriber turn on sucess");
    auto sub = node->create_subscription<sensor_msgs::msg::Imu>("/imu", 1000, ImuCallback);
    rclcpp::spin(node);
    rclcpp::shutdown();

    return 0;
}
