#!/usr/bin/env python
import rospy
import socket
from apple_catch.srv import DoorStatus, DoorStatusRequest, DoorStatusResponse


def handler(req):
    host = '127.0.0.1'
    port = 18899

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))
    client.send('door_status')

    responce = client.recv(1024)

    return DoorStatusResponse(float(responce))


def get_door_status():
    rospy.init_node('door_status')
    srv = rospy.Service('door_status', DoorStatus, handler)

    rospy.spin()


if __name__ == '__main__':
    get_door_status()
