#!/usr/bin/env python
import rospy
import socket
from apple_catch.srv import OpenDoor, OpenDoorRequest, OpenDoorResponse


def handler(req):
    host = '127.0.0.1'
    port = 18899

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))
    client.send('open_door {}'.format(req.time))

    responce = client.recv(1024)

    return OpenDoorResponse(responce)


def get_door_status():
    rospy.init_node('open_door')
    srv = rospy.Service('open_door', OpenDoor, handler)

    rospy.spin()


if __name__ == '__main__':
    get_door_status()
