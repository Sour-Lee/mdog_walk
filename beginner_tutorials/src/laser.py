#!/usr/bin/env python

import rospy
import numpy as np
from sensor_msgs.msg import LaserScan

count = 0

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
    '''

    #rospy.loginfo("I heard laser scan %s", data.header.seq)
 
    global count
    count += 1 
    print(count)

    with open("laser.txt",mode="a") as file :
        for i in range(len(data.ranges)) :
            #print(data.ranges[i])
            x1=float(format(data.ranges[i]*np.cos(data.angle_min+data.angle_increment*i),'.5f'))
            y1=float(format(data.ranges[i]*np.sin(data.angle_min+data.angle_increment*i),'.5f'))
            file.write(str(x1)+"  "+str(y1)+"\n")

    if count == 360 :
        rospy.signal_shutdown(count)

if __name__ == '__main__':
    rospy.init_node('listener', anonymous=True)
    rospy.Subscriber("/scan", LaserScan, laserCallback)
    rospy.spin()
