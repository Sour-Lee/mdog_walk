#!/usr/bin/env python

import rospy
from sensor_msgs.msg import Imu

def imu_cb(msg):
    rospy.loginfo("\norientation : \n%s",msg.orientation)
    print("-----------------------------")
    rospy.loginfo("\nangular_velocity : \n%s",msg.angular_velocity)
    print("-----------------------------")
    rospy.loginfo("\nlinear_acceleration : \n%s",msg.linear_acceleration)
    with open("data.txt",mode="a") as file : 
        file.write(str(msg.orientation)+"\n")
        file.write("-----------------------------\n")

if __name__ == '__main__':
    rospy.init_node('listener', anonymous=True)
    rospy.Subscriber("/imu/data", Imu, imu_cb)
    rospy.spin()
