#!/usr/bin/env python3
import rospy
import numpy as np
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion
from math import degrees
from enum import Enum

from sensor_msgs.msg import LaserScan

class State(Enum):
    
    #Init States, left turning, right turning, straight forward, stop then turn around
    LT = 1
    RT = 2
    SW = 3
    TURNROUND = 4

class task3:

    #Init range value
    ranges = None
    #Init function


class State(Enum):
    
    #Init States, left turning, right turning, staight forward, stop and turn around
    LT = 1
    RT = 2
    SW = 3
    TURNROUND = 4

class task3:

    
    #Init range value
    ranges = None

    
    #Init function
    def __init__(self):
        rospy.init_node('task3')
        self.posx = 0.0
        self.posy = 0.0
        self.yaw  = 0.0

        self.subscriber = rospy.Subscriber('/odom', Odometry, self.odom_convert)
        self.publisher  = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
        self.vel_cmd    = Twist()


        self.rate            = rospy.Rate(10)
        self.scan_subscriber = rospy.Subscriber('/scan', LaserScan, self.scan_callback)

        rospy.on_shutdown(self.shutdown_ops)
        self.main()


    
    #Function to round number in two decimal places
    def round(self, value, precision):
        value = int(value * (10**precision))

        return float(value) / (10**precision)

    
   # Function for moving speed setting
    def move_speed_setting(self, linear = 0.0, angular = 0.0):
        self.vel_cmd.linear.x  = linear
        self.vel_cmd.angular.z = angular


    #Function for data publishing
    def publish(self):
        self.publisher.publish(self.vel_cmd)

    
    #the Function of state calculation
    def state_cal(self, r):
        forward  = r[0]
        left  = r[-90]
        right  = r[90]
        backward  = r[180]
        front_right = r[55]
        front_left = r[-55]

        alpha           = 0.4
        side_threshold  = 0.7
        front_threshold = 0.6
        back_threshold  = 0.8

        r_prime    = np.array(r)
        close_count = float(np.count_nonzero(r_prime<=back_threshold)) / 360.0 * 100.0

        if (close_count > 75 and forward <= front_threshold and front_right <= alpha * 1.5):
            return State.TURNROUND
        elif (forward <= front_threshold and left <= side_threshold and right <= side_threshold and front_left <= alpha * 1.5 and front_right <= alpha * 1.5):
            return State.TURNROUND
        elif (forward <= front_threshold and backward <= back_threshold and right <= side_threshold and front_left <= alpha * 1.5 and front_right <= alpha * 1.5):
            return State.TURNROUND
        elif (forward <= front_threshold and left <= side_threshold and right <= side_threshold and front_left >= alpha * 1.5 and front_right <= alpha * 1.5):
            return State.LT
        elif (right <= side_threshold and front_right >= alpha * 1.5):
            return State.RT
        elif (right >= side_threshold and front_right >= alpha * 1.5):
            return State.RT
        elif (forward <= front_threshold and left >= side_threshold and right <= side_threshold and front_left >= alpha * 1.5 and front_right <= alpha * 1.5):
            return State.LT

        else:
            return State.SW

    #Function of convert data
    def odom_convert(self, odom_data):
        orientation = odom_data.pose.pose.orientation
        position    = odom_data.pose.pose.position
        (_, _, yaw) = euler_from_quaternion([orientation.x,
            orientation.y, orientation.z, orientation.w],'sxyz')

        self.yaw  = self.round(degrees(yaw), 4)
        self.posx = self.round(position.x, 4)
        self.posy = self.round(position.y, 4)

    def stop(self):
        self.move_speed_setting()
        self.publish()

    def scan_callback(self, scan_data):
        self.ranges = scan_data.ranges

    
    #Function to round number
    def round(self, value, precision):
        value = int(value * (10**precision))

        return float(value) / (10**precision)

    
   # Function for moving speed setting
    def move_speed_setting(self, linear = 0.0, angular = 0.0):
        self.vel_cmd.linear.x  = linear
        self.vel_cmd.angular.z = angular * -1


    #Function for data publishing
    def publish(self):
        self.publisher.publish(self.vel_cmd)

    
    #the Function of state calculation
    def state_cal(self, r):
        forward  = r[0]
        left  = r[-90]
        right  = r[90]
        backward  = r[180]
        front_right = r[55]
        front_left = r[-55]

        alpha           = 0.4
        side_threshold  = 0.7
        front_threshold = 0.6
        back_threshold  = 0.8

        r_prime    = np.array(r)
        close_count = float(np.count_nonzero(r_prime<=back_threshold)) / 360.0 * 100.0

        if (close_count > 75 and forward <= front_threshold and front_right <= alpha * 1.5):
            return State.TURNROUND
        elif (forward <= front_threshold and left <= side_threshold and right <= side_threshold and front_left <= alpha * 1.5 and front_right <= alpha * 1.5):
            return State.TURNROUND
        elif (forward <= front_threshold and backward <= back_threshold and right <= side_threshold and front_left <= alpha * 1.5 and front_right <= alpha * 1.5):
            return State.TURNROUND
        elif (forward <= front_threshold and left <= side_threshold and right <= side_threshold and front_left >= alpha * 1.5 and front_right <= alpha * 1.5):
            return State.LT
        elif (right <= side_threshold and front_right >= alpha * 1.5):
            return State.RT

        

        elif (right >= side_threshold and front_right >= alpha * 1.5):
            return State.RT

        elif (forward <= front_threshold and left >= side_threshold and right <= side_threshold and front_left >= alpha * 1.5 and front_right <= alpha * 1.5):
            return State.LT

        else:
            return State.SW

    #Function of convert data
    def odom_convert(self, odom_data):
        orientation = odom_data.pose.pose.orientation
        position    = odom_data.pose.pose.position
        (_, _, yaw) = euler_from_quaternion([orientation.x,
            orientation.y, orientation.z, orientation.w],'sxyz')

        self.yaw  = self.round(degrees(yaw), 4)
        self.posx = self.round(position.x, 4)
        self.posy = self.round(position.y, 4)

    def stop(self):
        self.move_speed_setting()
        self.publish()

    def scan_callback(self, scan_data):
        self.ranges = scan_data.ranges

    
    #Shutdown function
    def shutdown_ops(self):
        rospy.logwarn("Received a shutdown request.")
        self.stop()

    
    #Main loop function
    def main(self):
        while not (self.ranges):
            self.rate.sleep()
        while True:
            state = self.state_cal(self.ranges)
            if (np.amin(np.append(self.ranges[0:30], self.ranges[330:360])) <= 0.4 and (self.ranges[55] >= 0.4 or self.ranges[-55] >= 0.4)):
                self.move_speed_setting(0, 1)
            elif (state == State.SW):
                front_right = self.ranges[55]
                e  = 0.4 - front_right
                kp = 3
                self.move_speed_setting(0.25, kp *e)
            elif (state == State.RT):
                self.move_speed_setting(0.25, -0.9)

            elif (state == State.LT):
                self.move_speed_setting(0.25, 1.5)

            elif (state == State.TURNROUND):
                self.move_speed_setting(0,1.5)
            elif (state == State.RT or state == State.RT):
                self.move_speed_setting(0.25, -0.9)

            elif (state == State.LT or state == State.LT):
                self.move_speed_setting(0.25, 1.5)

            elif (state == State.TURNROUND):
                self.move_speed_setting(0, 1.5)

            else:
                self.move_speed_setting(0, 0)

            self.publish()
            self.rate.sleep()

if __name__ == '__main__':
    try:
        task3()
    except rospy.ROSInterruptException:
        pass