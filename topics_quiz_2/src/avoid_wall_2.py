#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan

def ck_callback(msg):
    ck_move = Twist()
    
    ck_fata = msg.ranges[0]
    ck_stanga = msg.ranges[90]
    ck_dreapta = msg.ranges[270]

    if ck_fata > 1.0:
        ck_move.linear.x = 0.2
        ck_move.angular.z = 0.0
    
    if ck_fata < 1.0:
        ck_move.linear.x = 0.0
        ck_move.angular.z = 0.5

    if ck_dreapta < 1.0:
        ck_move.linear.x = 0.0
        ck_move.angular.z = 0.5

    if ck_stanga < 1.0:
        ck_move.linear.x = 0.0
        ck_move.angular.z = -0.5

    ck_pub.publish(ck_move)

rospy.init_node('ck_topics_quiz_node')
ck_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
ck_sub = rospy.Subscriber('/scan', LaserScan, ck_callback)
rospy.spin()
