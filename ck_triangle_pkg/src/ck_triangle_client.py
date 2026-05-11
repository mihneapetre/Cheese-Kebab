#! /usr/bin/env python

import rospy
from ck_triangle_pkg.srv import CKTriangle, CKTriangleRequest

rospy.init_node('ck_triangle_client')

rospy.wait_for_service('/ck_triangle')

ck_service = rospy.ServiceProxy('/ck_triangle', CKTriangle)

ck_req = CKTriangleRequest()
ck_req.side = 2.0
ck_req.repetitions = 1

ck_result = ck_service(ck_req)

rospy.loginfo("Success: %s", ck_result.success)
