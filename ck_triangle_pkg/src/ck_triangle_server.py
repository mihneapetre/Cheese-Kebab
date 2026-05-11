#! /usr/bin/env python

import rospy
import math
from geometry_msgs.msg import Twist
from ck_triangle_pkg.srv import CKTriangle, CKTriangleResponse

ck_cmd_pub = None

def ck_move_straight(ck_speed, ck_distance):
    ck_twist = Twist()
    ck_twist.linear.x = ck_speed
    ck_duration = rospy.Duration(ck_distance / ck_speed)
    ck_start = rospy.Time.now()
    ck_rate = rospy.Rate(10)
    while rospy.Time.now() - ck_start < ck_duration:
        ck_cmd_pub.publish(ck_twist)
        ck_rate.sleep()
    ck_cmd_pub.publish(Twist())
    rospy.sleep(0.3)

def ck_turn_120():
    ck_twist = Twist()
    ck_twist.angular.z = 0.5
    ck_angle = (2.0 * math.pi) / 3.0
    ck_duration = rospy.Duration(ck_angle / 0.5)
    ck_start = rospy.Time.now()
    ck_rate = rospy.Rate(10)
    while rospy.Time.now() - ck_start < ck_duration:
        ck_cmd_pub.publish(ck_twist)
        ck_rate.sleep()
    ck_cmd_pub.publish(Twist())
    rospy.sleep(0.3)

def ck_triangle_callback(ck_req):
    try:
        for ck_rep in range(ck_req.repetitions):
            for ck_side in range(3):
                ck_move_straight(0.3, ck_req.side)
                ck_turn_120()
        return CKTriangleResponse(success=True)
    except Exception as ck_err:
        return CKTriangleResponse(success=False)

if __name__ == '__main__':
    rospy.init_node('ck_triangle_server')
    ck_cmd_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
    rospy.Service('/ck_triangle', CKTriangle, ck_triangle_callback)
    rospy.spin()
