#! /usr/bin/python

import math
import rospy
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist
import time

chaser_msg = None
initial_msg = None

def update_chaser_position(message):
    global chaser_msg
    chaser_msg = message

def update_initial_turtle_position(message):
    global initial_msg
    initial_msg  = message


def chase(velocity=0.5, dst_thresh=0.5):
    global chaser_msg, initial_msg
    if chaser_msg is None or initial_msg is None:
        return

    x0, y0 = chaser_msg.x, chaser_msg.y
    x1, y1 = initial_msg.x, initial_msg.y
    norm2 = math.sqrt((x1 - x0)**2 + (y1 - y0)**2)
    
    if norm2 < dst_thresh:
        return

    twist = Twist()
    twist.linear.x = velocity
    twist.angular.z = math.atan2(y1 - y0, x1 - x0) - chaser_msg.theta 
    chaser_msg, initial_msg = None, None
    chaser_publisher.publish(twist)

rospy.init_node("turtles")
rospy.Subscriber('/chaser/pose', Pose, update_chaser_position)
rospy.Subscriber('/turtle1/pose', Pose, update_initial_turtle_position)
chaser_publisher = rospy.Publisher('/chaser/cmd_vel', Twist, queue_size=10)

while not rospy.is_shutdown():
    chase()
    time.sleep(0.3)


