#!/usr/bin/env python
import roslib
import rospy
import math
import tf
from geometry_msgs.msg import Twist
from geometry_msgs.msg import PointStamped
from sensor_msgs.msg import LaserScan
from move_base_msgs.msg import MoveBaseAction


def get_angle_and_distance_in_map(curr, next):
    nx, ny, cx, cy = next.point.x, next.point.y, curr.point.x, curr.point.y
    theta = math.atan2(ny - cy, nx - cx)
    dist = math.sqrt((ny - cy)**2 + (nx - cx)**2)

    return theta, dist


def get_angle_and_distance_in_baselink(next):
    nx, ny = next.point.x, next.point.y
    theta = math.atan2(ny, nx)
    dist = math.sqrt(ny**2 + nx**2)

    return theta, dist


def create_point_stamp(x, y):
    ps = PointStamped()
    ps.header.stamp = rospy.Time.now()
    ps.header.frame_id = '/map'
    ps.point.x = x
    ps.point.y = y
    ps.point.z = 0

    return ps


def add_header(p):
    ps = PointStamped()
    ps.header.stamp = rospy.Time.now()
    ps.header.frame_id = '/map'
    ps.point = p

    return ps


def transform_map_to_baselink(point_in_map):
    listener = tf.TransformListener()
    listener.waitForTransform(
        '/map', '/base_link', rospy.Time(), rospy.Duration(5.0))
    while not rospy.is_shutdown():
        try:
            now = rospy.Time.now()
            point_in_map.header.stamp = now
            listener.waitForTransform(
                '/map', '/base_link', now, rospy.Duration(5.0))
            destination = listener.transformPoint(
                '/base_link', point_in_map)
            return destination
        except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException) as e:
            rospy.logerr(e)
            continue


def transform_baselink_to_map(point_in_baselink):
    listener = tf.TransformListener()
    listener.waitForTransform(
        '/base_link', '/map', rospy.Time(), rospy.Duration(5.0))
    while not rospy.is_shutdown():
        try:
            now = rospy.Time.now()
            point_in_baselink.header.stamp = now
            listener.waitForTransform(
                '/base_link', '/map', now, rospy.Duration(5.0))
            destination = listener.transformPoint(
                '/map', point_in_baselink)
            return destination
        except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException) as e:
            rospy.logerr(e)
            continue


def locate_position_in_map():
    listener = tf.TransformListener()
    rate = rospy.Rate(10.0)
    while not rospy.is_shutdown():
        try:
            now = rospy.Time.now()
            robot_in_base_link = PointStamped()
            robot_in_base_link.header.stamp = now
            robot_in_base_link.header.frame_id = "/base_link"
            robot_in_base_link.point.x = 0
            robot_in_base_link.point.y = 0
            robot_in_base_link.point.z = 0
            listener.waitForTransform(
                '/map', '/base_link', now, rospy.Duration(10.0))
            robot_in_map = listener.transformPoint('/map', robot_in_base_link)
            return robot_in_map
            # rospy.loginfo(robot_in_map)
            # rate.sleep()
        except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException) as e:
            rospy.logerr(e)
            continue


def rotate(rad, pub_vel, reverse=False):
    # if reverse=True, robot rotate in clock-direction
    runtime = rad
    start = rospy.Time.now()
    rate = rospy.Rate(10.0)
    cmdmsg = Twist()
    while not rospy.is_shutdown():
        now = rospy.Time.now()
        if (now - start > rospy.Duration(runtime)):
            cmdmsg.linear.x, cmdmsg.linear.y, cmdmsg.linear.z = 0, 0, 0
            cmdmsg.angular.x, cmdmsg.angular.y, cmdmsg.angular.z = 0, 0, 0
            pub_vel.publish(cmdmsg)
            break
        else:
            angle = max(-1, -rad) if reverse else min(1, rad)
            cmdmsg.linear.x, cmdmsg.linear.y, cmdmsg.linear.z = 0, 0, 0
            cmdmsg.angular.x, cmdmsg.angular.y, cmdmsg.angular.z = 0, 0, angle
            pub_vel.publish(cmdmsg)

        rate.sleep()

    cmdmsg.linear.x, cmdmsg.linear.y, cmdmsg.linear.z = 0, 0, 0
    cmdmsg.angular.x, cmdmsg.angular.y, cmdmsg.angular.z = 0, 0, 0
    pub_vel.publish(cmdmsg)


def is_apple_exists_in_map(apple_ps, laser_scan_msg):
    apple_ps_bl = map_to_baselink(apple_ps)
    apple_angle, apple_dist = get_angle_and_distance_baselink(apple_ps_bl)

    angle_min = laser_scan_msg.angle_min
    angle_increment = laser_scan_msg.angle_increment
    ranges = laser_scan_msg.ranges
    idx = int((apple_angle - angle_min) // angle_increment)

    delta = 10
    cond = []
    for i in range(max(0, idx - delta), min(len(ranges), idx + delta)):
        cond.append(ranges[i])
    laser_dist = min(cond)

    print(apple_angle)
    print(angle_min + idx * angle_increment)

    print(apple_dist)
    print(laser_dist)

    eps = 0.3
    try:
        diff = abs(apple_dist - laser_dist)
    except IndexError as e:
        rospy.logerr(e)
        return False

    if (diff < eps):
        return True
    else:
        return False


def move_to_in_map(ps, pub_vel):
    rate = rospy.Rate(10)
    while not rospy.is_shutdown():
        ps_bl = map_to_baselink(ps)
        theta, dist = get_angle_and_distance_baselink(ps_bl)

        eps = 0.5
        cmdmsg = Twist()
        speed = min(1.0, ps.point.x)
        angle = min(1.0, theta) if theta > 0 else max(-1.0, theta)

        if (dist < eps):
            cmdmsg.linear.x, cmdmsg.linear.y, cmdmsg.linear.z = 0, 0, 0
            cmdmsg.angular.x, cmdmsg.angular.y, cmdmsg.angular.z = 0, 0, 0
            pub_vel.publish(cmdmsg)
            break

        cmdmsg.linear.x, cmdmsg.linear.y, cmdmsg.linear.z = speed, 0, 0
        cmdmsg.angular.x, cmdmsg.angular.y, cmdmsg.angular.z = 0, 0, angle

        pub_vel.publish(cmdmsg)
        rate.sleep()
