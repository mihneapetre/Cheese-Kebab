#! /usr/bin/env python3
import rospy
import actionlib
from geometry_msgs.msg import Twist
from drone_action.msg import DroneAction, DroneFeedback, DroneResult, DroneGoal

class DroneServer(object):
    _feedback = DroneFeedback()
    _result = DroneResult()

    def __init__(self):
        self._as = actionlib.SimpleActionServer("drone_control", DroneAction, self.goal_callback, False)
        self.cmd_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
        self._as.start()
        
    def goal_callback(self, goal):
        C = goal.command
        K = Twist()

        if C == "TAKEOFF":
            K.linear.z = 0.5
            for i in range(3):
                self.cmd_pub.publish(K)
                self._feedback.status = "take off"
                self._as.publish_feedback(self._feedback)
                rospy.sleep(1)
            
            K.linear.z = 0.0
            self.cmd_pub.publish(K)
            
        elif C == "LAND":
            K.linear.z = -0.5
            for i in range(3):
                self.cmd_pub.publish(K)
                self._feedback.status = "landing"
                self._as.publish_feedback(self._feedback)
                rospy.sleep(1)
                
            K.linear.z = 0.0
            self.cmd_pub.publish(K)

        self._as.set_succeeded(self._result)

def cb(feedback):
    print(feedback.status)

if __name__ == '__main__':
    rospy.init_node('drone_action_server_node')
    
    server = DroneServer()
    
    C = actionlib.SimpleActionClient('drone_control', DroneAction)
    C.wait_for_server()
    
    K = DroneGoal()
    
    K.command = "TAKEOFF"
    C.send_goal(K, feedback_cb=cb)
    C.wait_for_result()
    
    rospy.sleep(5)
    
    K.command = "LAND"
    C.send_goal(K, feedback_cb=cb)
    C.wait_for_result()
