#!/usr/bin/env python
import roslib; roslib.load_manifest('missile_launcher')
import rospy
from std_msgs.msg import String
import dreamcheekystorm as dcs
import time

launcher = dcs.DreamCheekyStorm()

def callback(datamsg):
    data = datamsg.data
    rospy.loginfo("Received launcher command: " + str(data))
    if data == "u":
        launcher.up()
    elif data == "d":
        launcher.down()
    elif data == "l":
        launcher.left()
    elif data == "r":
        launcher.right()
    elif data == "s":
        launcher.stop()
    elif data == "f":
        launcher.fire()
    elif data == "h":
        launcher.home()

def missile_listener():
    rospy.init_node('missile', anonymous=True)
    rospy.Subscriber('missile_launcher', String, callback)
    rospy.spin()
    
if __name__ == '__main__':
    missile_listener()
