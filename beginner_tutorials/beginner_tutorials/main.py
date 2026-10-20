#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
import numpy as np
from numpy import linalg as npla
from numpy.linalg import inv
from sensor_msgs.msg import LaserScan
from visualization_msgs.msg import Marker
from std_msgs.msg import Float64MultiArray

marker = Marker()
node = None

############################# golbal variables #############################
counter = 0 # golbal
position = np.array([]) #golbal
Yaw_p = np.array([]) #golbal
T = 0.125
W = np.array([ [T*T/2,0],[T,0],[0,T*T/2],[0,T] ])
R = np.matmul(W,W.T)*0.185
cov_c = R #golbal
############################# golbal variables #############################

############################# rviz #############################
def init_maker() : 

    marker.header.frame_id = "/laser_link"
    marker.header.stamp = node.get_clock().now().to_msg()

    global position
    if position.size > 0 :
        x=position[0];
        y=position[2];
    else : 
        x = 0
        y = 0

    # set shape, Arrow: 0; Cube: 1 ; Sphere: 2 ; Cylinder: 3
    marker.type = 3
    marker.id = 0

    # Set the scale of the marker
    marker.scale.x = 0.2
    marker.scale.y = 0.2
    marker.scale.z = 1.5

    # Set the color
    marker.color.r = 0.0
    marker.color.g = 1.0
    marker.color.b = 0.0
    marker.color.a = 1.0

    # Set the pose of the marker
    marker.pose.position.x = x
    marker.pose.position.y = y
    marker.pose.position.z = 0.75
    marker.pose.orientation.x = 0.0
    marker.pose.orientation.y = 0.0
    marker.pose.orientation.z = 0.0
    marker.pose.orientation.w = 1.0

    marker.lifetime.sec = 0
    marker.lifetime.nanosec = 100000000
    node.marker_pub.publish(marker)
############################# rviz #############################



############################# Segment #############################
def Segment(data_list):
    x = data_list[:,0]
    y = data_list[:,1]
    
    threshold = 0.1
    
    S_i = 1 # size of segment
    S_n = 0 # number(index) of segment
    n0ind = np.where(np.abs(x)+np.abs(y)!=0)[0]
    n_s = len(n0ind)
    n_0 = n_s
    
    Seg = [[]]
    Seg[0].append(n0ind[0])
    
    for i in range(1,n_0):
        if np.sqrt( np.square( x[n0ind[i]] -  x[n0ind[i-1]] ) + np.square( y[n0ind[i]] -  y[n0ind[i-1]] ) ) < threshold:
            S_i = S_i + 1
            Seg[S_n].append(n0ind[i])
        else:
            Seg.append([])
            S_i = 1
            S_n = S_n + 1
            Seg[S_n].append(n0ind[i])
            
    Si_n = []
    S_n = S_n + 1  # the index starts from 0 but we want the number of segment
    for j in range(S_n):
        k = len( Seg[:][j] )
        Si_n.append(k)
        
    Seg = np.array(Seg,dtype = object).T
    Si_n = np.array(Si_n)
    
    return Seg, Si_n, S_n
############################# Segment #############################


############################# classifier #############################

### 1 ###
def classifier1(data_list, time): 
    training_data = []
    for i in range(time[0],time[1]):
        Si_n = Segment(data_list[i,:,:])[1]
        S_n = Segment(data_list[i,:,:])[2]
        for j in range(S_n):
            if Si_n[j] <= 17 and Si_n[j] >= 6:
                training_data.append(1)
            else:
                training_data.append(-1) 
    training_data = np.array(training_data)
    return training_data

### 2 ###
def classifier2(data_list, time):
    training_data = []
    std = []
    k = -1
    for i in range(time[0],time[1]):
        Seg = Segment(data_list[i,:,:])[0]
        Si_n = Segment(data_list[i,:,:])[1]
        S_n = Segment(data_list[i,:,:])[2]
        for j in range(S_n):
            k = k + 1
            mean_x = np.mean( data_list[i,Seg[j],0] )
            mean_y = np.mean( data_list[i,Seg[j],1] )
            x_dfm = np.square( data_list[i,Seg[j],0] - mean_x ) # x data deviation from mean
            y_dfm = np.square( data_list[i,Seg[j],1] - mean_y ) # y data deviation from mean
            std.append( np.sqrt( np.sum(x_dfm + y_dfm) / len(x_dfm) ) )
            if std[k] <= 0.037 and std[k] >= 0.001: 
                training_data.append(1)
            else:
                training_data.append(-1)
    training_data = np.array(training_data)
    return training_data

### 3 ###
def classifier3(data_list, time): 
    training_data = []
    Max_W = []
    k = -1
    for i in range(time[0],time[1]):
        Seg = Segment(data_list[i,:,:])[0]
        Si_n = Segment(data_list[i,:,:])[1]
        S_n = Segment(data_list[i,:,:])[2]
        for j in range(S_n):
            k = k + 1
            x = data_list[i,Seg[j],0]
            y = data_list[i,Seg[j],1]
            Max_W.append( np.sqrt( np.square( x[0]-x[-1] )+np.square( y[0]-y[-1] ) ) )
            if Max_W[k] >= 0.03 and  Max_W[k] <= 0.11:
                training_data.append(1)
            else :
                training_data.append(-1)
    training_data = np.array(training_data)
    return training_data

### 4 ###
def classifier4_5(data_list, time):
    training_data_Sc = []
    training_data_Rc = []
    Rc = []
    Sc = []
    k = -1
    for i in range(time[0],time[1]):
        Seg = Segment(data_list[i,:,:])[0]
        Si_n = Segment(data_list[i,:,:])[1]
        S_n = Segment(data_list[i,:,:])[2]
        for j in range(S_n):
            k = k + 1
            x = data_list[i,Seg[j],0]
            y = data_list[i,Seg[j],1]
            A1 = -2*x
            A2 = -2*y
            A3 = np.ones(Si_n[j],dtype = np.int64)
            A = np.vstack((A1,A2,A3)).T
            x_square = np.square( data_list[i,Seg[j],0] )
            y_square = np.square( data_list[i,Seg[j],1] )
            b = -x_square - y_square
            X = np.matmul(np.matmul( np.linalg.pinv( np.matmul(A.T,A) ) , A.T) , b)
            Rc.append( np.real( np.sqrt( np.square(X[0]) + np.square(X[1]) - X[2] ) ) )
            Sc.append( np.sum( np.square( Rc[j] - np.sqrt( np.square( X[0] - x) + np.square( X[1] - y) ) ) ) )
            if Sc[k] >= 0.00000385 and Sc[k] <= 0.00016:
                training_data_Sc.append(1)
            else:
                training_data_Sc.append(-1)
            
            if Rc[k] >= 0.04 and Rc[k] <= 0.124:
                training_data_Rc.append(1)
            else:
                training_data_Rc.append(-1)
    training_data_Sc = np.array(training_data_Sc)
    training_data_Rc = np.array(training_data_Rc)
    return training_data_Sc, training_data_Rc

### 5 ###
def classifier6(data_list, time): 
    training_data = []
    pos = []
    mean_angular = []
    k = -1
    for i in range(time[0],time[1]):
        Seg = Segment(data_list[i,:,:])[0]
        Si_n = Segment(data_list[i,:,:])[1]
        S_n = Segment(data_list[i,:,:])[2]
        for j in range(S_n):
            k = k + 1
            x = data_list[i,Seg[j],0]
            y = data_list[i,Seg[j],1]


            pos = np.append(x,y)
            # print(pos)
            # print(Si_n[i])
            beta = []
            for s in range(1,Si_n[j]-1):
                # print(pos[s])
                vec1 = pos[s] - pos[s-1]
                vec2 = pos[s+1] - pos[s]
                inner_product = np.dot(vec1,vec2)
                cos_val = inner_product / npla.norm(vec1) / npla.norm(vec2)
                beta.append(np.arccos(cos_val))
            mean_angular.append(np.sum(beta) / S_n)
            if mean_angular[k] >= 0.037 and mean_angular[k] <= 0.0436:
                training_data.append(1)
            elif mean_angular[k] >= 0.1111 and mean_angular[k] <= 0.1112:
                training_data.append(1)
            elif mean_angular[k] >= 0.14 and mean_angular[k] <= 0.1667:
                training_data.append(1)
            elif mean_angular[k] >= 0.1428 and mean_angular[k] <= 0.6:
                training_data.append(1)
            elif mean_angular[k] >= 0.642 and mean_angular[k] <= 0.8333:
                training_data.append(1)
            else :
                training_data.append(-1)
    training_data = np.array(training_data)
    return training_data
############################# classifier #############################


############################# Strong classifier #############################
def class_foot(data_list,time):
    f1 = 0.457410390937889 * classifier1(data_list,time)
    f2 = 0.701214655657343 * classifier2(data_list,time)
    f3 = 0.419908412213672 * classifier3(data_list,time)
    f4 = 0.243733541969582 * classifier4_5(data_list,time)[0]
    f5 = 0.942289936041347 * classifier4_5(data_list,time)[1]
    f6 = 0.008098171903908 * classifier6(data_list,time)    
    F = np.sign( f1 + f2 + f3 + f4 + f5 + f6)
    
    return F
############################# Strong classifier #############################


############################# Kalman filter #############################
def kf(data_list,Yaw_p,cov_c,H,position):
    T = 0.125
    u = 0.008
    A = np.array([ [1,T,0,0],[0,1,0,0],[0,0,1,T],[0,0,0,1] ])
    W = np.array([ [T*T/2,0],[T,0],[0,T*T/2],[0,T] ])
    R = np.matmul(W,W.T)*0.185
    B = np.array([T*T/2,T,T*T/2,T]).T
    C = np.array([ [1,0,0,0],[0,0,1,0] ])
    I = np.identity(4)
    Q = 0.025*np.identity(2)

    Seg = Segment(data_list[0,:,:])[0]
    Si_n = Segment(data_list[0,:,:])[1]
    S_n = Segment(data_list[0,:,:])[2]
    leg_seg = np.array([])
    k = 0
    
    for i in range(S_n):
        if H[k] == 1:
            leg_mean = np.array(np.mean(data_list[0,Seg[i],:],axis = 0))
            # print(leg_mean)
            if leg_seg.size == 0 :
                leg_seg = np.append(leg_seg,leg_mean,axis = 0)
            else : 
                leg_seg = np.vstack((leg_seg,leg_mean))
                # print(leg_seg)
        k = k + 1
        
    if leg_seg.size == 0:
        x1 = np.array([Yaw_p[0],Yaw_p[2]])
    elif leg_seg.size == 2:
        x1 = leg_seg
    else :
        x1 = np.array([])
        for j in range(len(leg_seg)-1):
            for s in range(j+1,len(leg_seg)):
                leg_center = np.mean(leg_seg[(j,s),:],axis = 0)
                leg_range = np.sqrt(sum(np.square(leg_seg[j,:]-leg_seg[s,:])))
                if leg_range < 0.5:
                    if x1.size == 0 :
                        x1 = np.append(x1,leg_center,axis = 0)
                    else : 
                        x1 = np.vstack((x1,leg_center))

        if x1.size == 0 :
            x1 = leg_seg
        else : 
            x1 = np.vstack((leg_seg,x1))
    

    # kalman filter
    Dm = []
    Yaw_p = np.matmul(A,Yaw_p) + B*u
    cov_c = np.matmul(np.matmul(A,cov_c),A.T) + R
    # print(Yaw_p)
    # data association
    if x1.size > 0:
        sigma = np.matmul(np.matmul(C,cov_c),C.T) + Q
        for i in range(int(x1.size/2)):

            if x1.size == 2 :
                dis = x1 - np.matmul(C,Yaw_p)
            else : 
                dis = x1[i,:] - np.matmul(C,Yaw_p)

            Dm.append(np.sqrt(np.matmul(np.matmul(dis,inv(sigma)),dis)))
        minD = np.min(Dm)
        ind = np.argmin(Dm)
        if minD <= 3.85:
            K = np.matmul(np.matmul(cov_c,C.T),inv(sigma))

            if x1.size == 2 :
                Yaw_p = Yaw_p + np.matmul(K,(x1-np.matmul(C,Yaw_p)))
            else : 
                Yaw_p = Yaw_p + np.matmul(K,(x1[ind,:]-np.matmul(C,Yaw_p)))
            
            cov_c = np.matmul((I-np.matmul(K,C)),cov_c)
            position = Yaw_p
            
    position = position
    return Yaw_p, cov_c, position
############################# Kalman filter #############################

def laserCallback(data):
    
    ################## global variables ##################
    global counter
    global Yaw_p
    global position
    global cov_c

    ################## input data ##################
    x=[]
    y=[]
    #print(len(data.ranges))
    
    for i in range(len(data.ranges)) :
        #print(len(data.ranges))
        x1=float(format(data.ranges[i]*np.cos(data.angle_min+data.angle_increment*i),'.5f'))
        y1=float(format(data.ranges[i]*np.sin(data.angle_min+data.angle_increment*i),'.5f'))
        angle = data.angle_min+data.angle_increment*i
        if data.ranges[i] <= 2 and (angle <= -2.79 or angle >= 2.79) :
            x.append(x1)
            y.append(y1)

    x=np.array(x)
    y=np.array(y)
    x_y_data=np.vstack((x,y)).T
    data_list = x_y_data.reshape(1,len(x),2)

    ################## adaboost ##################
    time = [0,1]
    H = class_foot(data_list,time)

    ################## Tracking ##################
    if counter == 0 :
        Seg = Segment(data_list[0,:,:])[0]
        Si_n = Segment(data_list[0,:,:])[1]
        S_n = Segment(data_list[0,:,:])[2]
        leg_seg = np.array([])
        k = 0
        
        for i in range(S_n):
            if H[k] == 1:
                leg_mean = np.array(np.mean(data_list[0,Seg[i],:],axis = 0))
                seg_range = np.sqrt(sum(np.square(leg_mean)))
                if seg_range <=2 :
                    # print(leg_mean) 
                    if leg_seg.size == 0 :
                        leg_seg = np.append(leg_seg,leg_mean,axis = 0)
                    else : 
                        leg_seg = np.vstack((leg_seg,leg_mean))
                    # print(leg_seg)
            k = k + 1
            
        if leg_seg.size == 0:
            x1 = np.array([])
            Yaw_p = np.array([0 , 0 , 0 , 0])
        elif leg_seg.size == 2:
            x1 = leg_seg
            Yaw_p = np.array([x1[0] , 0 , x1[1] , 0])
        else :
            x1 = np.array([])
            for j in range(len(leg_seg)-1):
                for s in range(j+1,len(leg_seg)):
                    leg_center = np.mean(leg_seg[(j,s),:],axis = 0)
                    leg_range = np.sqrt(sum(np.square(leg_seg[j,:]-leg_seg[s,:])))
                    if leg_range < 0.5:
                        if x1.size == 0 :
                            x1 = np.append(x1,leg_center,axis = 0)
                        else : 
                            x1 = np.vstack((x1,leg_center))

            if x1.size == 0 :
                x1 = leg_seg
            else : 
                x1 = np.vstack((leg_seg,x1))

            init = np.power(x1,2)
            init = np.sqrt(init[:,0]+init[:,1])
            init = np.argmin(init)
            Yaw_p = np.array([x1[init,0] , 0 , x1[init,1] , 0])
	
        #dis = np.sqrt(np.power(Yaw_p[0],2)+np.power(Yaw_p[2],2))
        #if dis <= 2 :      
        fusion = kf(data_list,Yaw_p,cov_c,H,position)
        Yaw_p = fusion[0]
        cov_c = fusion[1]
        position = fusion[2]       
        counter = counter + 1

    else : 
        #dis = np.sqrt(np.power(Yaw_p[0],2)+np.power(Yaw_p[2],2))
        #if dis <= 2 : 
        fusion = kf(data_list,Yaw_p,cov_c,H,position)
        Yaw_p = fusion[0]
        cov_c = fusion[1]
        position = fusion[2]
        counter = counter + 1
        init_maker()

    ################## Tracking #################

    print("x-axis = "+str(Yaw_p[0]),"y-axis = "+str(Yaw_p[2]),sep="\n")
    print("dis = ",np.sqrt(np.power(Yaw_p[0],2)+np.power(Yaw_p[2],2)))
    print("===============================================================")
    
    if counter == 3600 :
        rclpy.shutdown()

    ################## Publisher #################
    if rclpy.ok():
        publisher()


def publisher():
    global position
    if position.size > 0 :
        x=position[0]
        y=position[2]
    else : 
        x = 0
        y = 0
    msg = Float64MultiArray()  # the data to be sent, initialise the array
    msg.data = [float(x), float(y)] # assign the array with the value you want to send
    node.direction_pub.publish(msg)


class LaserTracker(Node):
    def __init__(self):
        super().__init__("laser_tracker")
        self.marker_pub = self.create_publisher(Marker, "/visualization_marker", 2)
        self.direction_pub = self.create_publisher(Float64MultiArray, "/direction_msg", 10)
        self.subscription = self.create_subscription(LaserScan, "/scan", laserCallback, 10)


def main(args=None):
    global node
    rclpy.init(args=args)
    node = LaserTracker()
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
