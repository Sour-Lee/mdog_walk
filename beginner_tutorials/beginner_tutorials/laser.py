#!/usr/bin/env python

import rclpy
from rclpy.node import Node
import numpy as np
from sensor_msgs.msg import LaserScan

count = 0
node = None

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

    # node.get_logger().info("I heard laser scan")
 
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
        rclpy.shutdown()


class LaserListener(Node):
    def __init__(self):
        super().__init__("laser_listener")
        self.subscription = self.create_subscription(LaserScan, "/scan", laserCallback, 10)


def main(args=None):
    global node
    rclpy.init(args=args)
    node = LaserListener()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        node = None
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == "__main__":
    main()
