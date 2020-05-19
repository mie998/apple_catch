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
    pi = math.pi
    ring = positions.ring_pos
    fixed = positions.fixed_pos

    rotate(pi, pub_vel, reverse=True)
    move_to_in_map(add_header(ring[0]), pub_vel)
    rotate(pi / 2, pub_vel, reverse=True)

    move_to_in_map(add_header(fixed[0]), pub_vel)
    rotate(pi / 2, pub_vel)

    move_to_in_map(add_header(fixed[1]), pub_vel)
    move_to_in_map(add_header(ring[1]), pub_vel)
    rotate(pi, pub_vel)
    move_to_in_map(add_header(ring[2]), pub_vel)
    move_to_in_map(add_header(ring[3]), pub_vel)

    rotate(pi/3, pub_vel)
    move_to_in_map(add_header(ring[5]), pub_vel)
    rotate(pi/2, pub_vel)

    move_to_in_map(add_header(ring[4]), pub_vel)
    move_to_in_map(add_header(fixed[3]), pub_vel)

    open_door(10)
    rotate(pi*2/3, pub_vel, reverse=True)

# section 2
    if(door_status()):
        move_to_in_map(add_header(fixed[4]), pub_vel)
    else:
        open_door(10)
        rospy.Rate(100).sleep()
        move_to_in_map(add_header(fixed[4]), pub_vel)

    move_to_in_map(add_header(fixed[5]), pub_vel)
    rotate(pi / 2, pub_vel)

    move_to_in_map(add_header(ring[6]), pub_vel)
    rotate(pi / 2, pub_vel, reverse=True)

    move_to_in_map(add_header(ring[7]), pub_vel)
    rotate(pi * 2 / 3, pub_vel, reverse=True)

    move_to_in_map(add_header(ring[8]), pub_vel)
    rotate(pi * 2 / 3, pub_vel, reverse=True)

    move_to_in_map(add_header(ring[9]), pub_vel)
    move_to_in_map(add_header(ring[10]), pub_vel)
    rotate(pi * 2 / 3, pub_vel, reverse=True)

# section 3
    move_to_in_map(add_header(fixed[8]), pub_vel)
    rotate(pi * 2 / 3, pub_vel)

    move_to_in_map(add_header(ring[11]), pub_vel)
    move_to_in_map(add_header(ring[12]), pub_vel)
    rotate(pi * 3 / 4, pub_vel)

    move_to_in_map(add_header(ring[13]), pub_vel)
    rotate(pi / 2, pub_vel)
    move_to_in_map(add_header(fixed[10]), pub_vel)
    rotate(pi / 3, pub_vel, reverse=True)
    move_to_in_map(add_header(ring[14]), pub_vel)  # goal


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
