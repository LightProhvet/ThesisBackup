cmake_minimum_required(VERSION 2.8.3)
project(semantic_segmentation)

## Find catkin macros and libraries
## if COMPONENTS list like find_package(catkin REQUIRED COMPONENTS xyz)
## is used, also find other catkin packages
find_package(ament_cmake REQUIRED)
find_package(ament_python REQUIRED)
find_package(rclcpp REQUIRED)
find_package(rclpy REQUIRED)
find_package(std_msgs REQUIRED)

add_executable(semantic_segmentation nodes/segmentation_node.py)
ament_target_dependencies(semantic_segmentation rclpy std_msgs)



install(TARGETS
nodes/segmentation_node
nodes/models
DESTINATION lib/${PROJECT_NAME})

ament_package()
