#!/usr/bin/env python3

import rclpy
import math
from builtin_interfaces.msg import Duration
from rclpy.node import Node
from std_msgs.msg import String
from sensor_msgs.msg import Imu
from sensor_msgs.msg import LaserScan
from visualization_msgs.msg import Marker

RAD2DEG = lambda x: ((x)*180/math.pi)
counter=0

marker_pub = None
marker = Marker()
shape = Marker.CYLINDER
node = None


def callback1():
    global counter, marker, marker_pub, shape, RAD2DEG
    x=1.0*math.cos(0.174*counter)
    y=1.0*math.sin(0.174*counter)
    marker.pose.position.x = x
    marker.pose.position.y = y
    #node.get_logger().info("x={},y={}".format(x,y))
    counter += 1

    marker_pub.publish(marker);
    
def scanCallback(scan):
    global counter, marker, marker_pub, shape, RAD2DEG
    count = int(round(scan.scan_time / scan.time_increment))
    print("[YDLIDAR INFO]: I heard a laser scan {}[{}]:".format(scan.header.frame_id, count))
    print("[YDLIDAR INFO]: I heard a laser scan {}[{}]:".format(scan.header.frame_id, len(scan.ranges)))
    '''
    print("[YDLIDAR INFO]: angle_range : [{}, {}]".format(RAD2DEG(scan.angle_min), RAD2DEG(scan.angle_max)))
 
    for i in range(count): 
        degree = RAD2DEG(scan.angle_min + scan.angle_increment * i)
        if(degree > -5 and degree< 5):
            print("[YDLIDAR INFO]: angle-distance : [{}, {}, {}]".format( degree, scan.ranges[i], i))
    '''

    
def init_marker():
    global counter, marker, marker_pub, shape, RAD2DEG
    # Initialize maker's setting.
    # Set the frame ID and timestamp.  See the TF tutorials for information on these.
    marker.header.frame_id = "/target"
    marker.header.stamp = node.get_clock().now().to_msg()

    # Set the namespace and id for this marker.  This serves to create a unique ID
    # Any marker sent with the same namespace and id will overwrite the old one
    marker.ns = "basic_shapes"
    marker.id = 0;
    # Set the marker type.  Initially this is CUBE, and cycles between that and SPHERE, ARROW, and CYLINDER
    marker.type = shape

    # Set the marker action.  Options are ADD, DELETE, and new in ROS Indigo: 3 (DELETEALL)
    # Tag(ACTION)
    marker.action = Marker.ADD

    # Set the pose of the marker.  This is a full 6DOF pose relative to the frame/time specified in the header
    #Tag(POSE)
    marker.pose.position.x = 0
    marker.pose.position.y = 0
    marker.pose.position.z = 0
    marker.pose.orientation.x = 0.0
    marker.pose.orientation.y = 0.0
    marker.pose.orientation.z = 0.0
    marker.pose.orientation.w = 1.0

    # Set the scale of the marker -- 1x1x1 here means 1m on a side
    marker.scale.x = 0.1
    marker.scale.y = 0.1
    marker.scale.z = 0.2

    # Set the color -- be sure to set alpha to something non-zero!
    marker.color.r = 0.0
    marker.color.g = 1.0
    marker.color.b = 0.0
    marker.color.a = 1.0

    #Tag(LIFETIME)
    marker.lifetime = Duration()
    
    
if __name__ == "__main__":
    rclpy.init()
    node = Node("talker")
    marker_pub = node.create_publisher(Marker, "visualization_marker", 1)
    #rate = rclpy.Rate(1)
    sub = node.create_subscription(LaserScan, "/scan", scanCallback, 1000)
    timer1 = node.create_timer(0.1, callback1)
    init_marker()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()
    
    
