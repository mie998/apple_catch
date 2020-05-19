#!/usr/bin/env python

import sys
import rospy
from apple_catch.srv import *


def open_door(time):
    rospy.wait_for_service('open_door')
    try:
        open_door = rospy.ServiceProxy('open_door', OpenDoor)
        resp = open_door(time)
        rospy.loginfo(resp)
    except rospy.ServiceException, e:
        print "Service call failed: %s" % e


def door_status():
    rospy.wait_for_service('door_status')
    try:
        door_status = rospy.ServiceProxy('door_status', DoorStatus)
        resp = door_status()
        rospy.loginfo(resp)
        True if resp.status > 0.5 else False
    except rospy.ServiceException, e:
        print "Service call failed: %s" % e
