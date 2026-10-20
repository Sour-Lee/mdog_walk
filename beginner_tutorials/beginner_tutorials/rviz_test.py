#!/usr/bin/env python

import rclpy
from rclpy.node import Node
import numpy as np
from sensor_msgs.msg import LaserScan
from visualization_msgs.msg import Marker


marker = Marker()
node = None
count = 0


def init_maker() : 

    marker.header.frame_id = "/laser_link"
    marker.header.stamp = node.get_clock().now().to_msg()

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

    marker.lifetime.sec = 0
    marker.lifetime.nanosec = 100000000
    node.marker_pub.publish(marker)



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
    node.get_logger().info("I heard laser scan")
    global count
    count += 1 
    print(count)
	

    init_maker()

    if count == 3600:
        rclpy.shutdown()


class RvizTest(Node):
    def __init__(self):
        super().__init__("rviz_test")
        self.marker_pub = self.create_publisher(Marker, "/visualization_marker", 2)
        self.subscription = self.create_subscription(LaserScan, "/scan", laserCallback, 10)


def main(args=None):
    global node
    rclpy.init(args=args)
    node = RvizTest()
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





