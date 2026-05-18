cmake_minimum_required(VERSION 3.0.2)
project(drone_action)

find_package(catkin REQUIRED COMPONENTS
  actionlib
  actionlib_msgs
  geometry_msgs
  rospy
  std_msgs
)

add_action_files(FILES Drone.action)
generate_messages(DEPENDENCIES actionlib_msgs std_msgs)
catkin_package(CATKIN_DEPENDS actionlib actionlib_msgs geometry_msgs rospy std_msgs)
include_directories(${catkin_INCLUDE_DIRS})
