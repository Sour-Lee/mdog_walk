#!/usr/bin/env python

import rospy
import numpy as np
from sensor_msgs.msg import LaserScan
from visualization_msgs.msg import Marker


marker = Marker()
marker_pub = rospy.Publisher("/visualization_marker", Marker, queue_size = 2)
count = 0


def init_maker() : 

    marker.header.frame_id = "/laser_link"
    marker.header.stamp = rospy.Time.now()

    global count
    x=1*np.cos(0.174*count);
    y=1*np.sin(0.174*count);

    # set shape, Arrow: 0; Cube: 1 ; Sphere: 2 ; Cylinder: 3
    marker.type = 1
    marker.id = 0

    # Set the scale of the marker
    marker.scale.x = 0.1
    marker.scale.y = 0.1
    marker.scale.z = 0.2

    # Set the color
    marker.color.r = 0.0
    marker.color.g = 1.0
    marker.color.b = 0.0
    marker.color.a = 1.0

    # Set the pose of the marker
    marker.pose.position.x = x
    marker.pose.position.y = y
    marker.pose.position.z = 0
    marker.pose.orientation.x = 0.0
    marker.pose.orientation.y = 0.0
    marker.pose.orientation.z = 0.0
    marker.pose.orientation.w = 1.0

    marker_pub.publish(marker)
    marker.lifetime = rospy.Duration(0.1)



def laserCallback(data):
    ''' 
    x=[]
    y=[]
    print(len(data.ranges))
    
    for i in range(len(data.ranges)) :
        #print(data.ranges[i])
        x1=float(format(data.ranges[i]*np.cos(data.angle_min+data.angle_increment*i),'.5f'))
        y1=float(format(data.ranges[i]*np.sin(data.angle_min+data.angle_increment*i),'.5f'))
        x.append(x1)
        y.append(y1)

    x=np.array(x)
    y=np.array(y)
    x_y_data=np.vstack((x,y)).T



 
    with open("laser.txt",mode="a") as file :
        for i in range(len(data.ranges)) :
            #print(data.ranges[i])
            x1=float(format(data.ranges[i]*np.cos(data.angle_min+data.angle_increment*i),'.5f'))
            y1=float(format(data.ranges[i]*np.sin(data.angle_min+data.angle_increment*i),'.5f'))
            file.write(str(x1)+"  "+str(y1)+"\n")
    '''
    rospy.loginfo("I heard laser scan %s", data.header.seq)
    global count
    count += 1 
    print(count)
	

    init_maker()

    if count == 3600 :
        rospy.signal_shutdown(count)

    

if __name__ == '__main__':
    rospy.init_node('listener', anonymous=True)
    rospy.Subscriber("/scan", LaserScan, laserCallback)
    r = rospy.Rate(10)
    rospy.spin()





