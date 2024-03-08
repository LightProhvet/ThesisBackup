// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from robot_ros2_msgs:msg/Encoders.idl
// generated code does not contain a copyright notice

#ifndef ROBOT_ROS2_MSGS__MSG__DETAIL__ENCODERS__STRUCT_H_
#define ROBOT_ROS2_MSGS__MSG__DETAIL__ENCODERS__STRUCT_H_

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

/// Struct defined in msg/Encoders in the package robot_ros2_msgs.
typedef struct robot_ros2_msgs__msg__Encoders
{
  std_msgs__msg__Header header;
  /// wheel speeds in
  float right_front;
  float left_front;
  float left_back;
  float right_back;
} robot_ros2_msgs__msg__Encoders;

// Struct for a sequence of robot_ros2_msgs__msg__Encoders.
typedef struct robot_ros2_msgs__msg__Encoders__Sequence
{
  robot_ros2_msgs__msg__Encoders * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} robot_ros2_msgs__msg__Encoders__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // ROBOT_ROS2_MSGS__MSG__DETAIL__ENCODERS__STRUCT_H_
