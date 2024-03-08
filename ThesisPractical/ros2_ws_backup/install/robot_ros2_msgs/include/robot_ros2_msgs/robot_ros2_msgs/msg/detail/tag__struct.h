// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from robot_ros2_msgs:msg/Tag.idl
// generated code does not contain a copyright notice

#ifndef ROBOT_ROS2_MSGS__MSG__DETAIL__TAG__STRUCT_H_
#define ROBOT_ROS2_MSGS__MSG__DETAIL__TAG__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'header'
#include "std_msgs/msg/detail/header__struct.h"
// Member 'pose'
#include "geometry_msgs/msg/detail/pose__struct.h"

/// Struct defined in msg/Tag in the package robot_ros2_msgs.
typedef struct robot_ros2_msgs__msg__Tag
{
  std_msgs__msg__Header header;
  /// distance to the next tag
  float distance;
  /// pose of the tag in world frame
  geometry_msgs__msg__Pose pose;
  /// specifies the floor at which tag is located
  int16_t floor;
  /// number that specifies tag
  int16_t id;
} robot_ros2_msgs__msg__Tag;

// Struct for a sequence of robot_ros2_msgs__msg__Tag.
typedef struct robot_ros2_msgs__msg__Tag__Sequence
{
  robot_ros2_msgs__msg__Tag * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} robot_ros2_msgs__msg__Tag__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // ROBOT_ROS2_MSGS__MSG__DETAIL__TAG__STRUCT_H_
