#!/usr/bin/env python
from geometry_msgs.msg import Twist
from geometry_msgs.msg import PointStamped
from sensor_msgs.msg import LaserScan
from move_base_msgs.msg import MoveBaseAction
from utils import *
from positions import positions
from door_client import *
import rospy
import tf
import math


def callback(msg):
    ring = positions.ring_pos
    if (is_apple_exists_in_map(add_header(ring[1]), msg)):
        print("apple found 1")

    print('')
    if (is_apple_exists_in_map(add_header(ring[2]), msg)):
        print("apple found 2")


def move():
    rospy.init_node('move')
    # rospy.Subscriber('clicked_point', PointStamped, callback)
    rospy.Subscriber('scan', LaserScan, callback)

    global pub_pt, pub_vel
    pub_pt = rospy.Publisher('closest_point', PointStamped, queue_size=10)
    pub_vel = rospy.Publisher('cmd_vel', Twist, queue_size=10)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()


if __name__ == '__main__':
    move()
