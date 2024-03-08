// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from robot_ros2_msgs:msg/PreviousAndNextPoint.idl
// generated code does not contain a copyright notice

#ifndef ROBOT_ROS2_MSGS__MSG__DETAIL__PREVIOUS_AND_NEXT_POINT__STRUCT_H_
#define ROBOT_ROS2_MSGS__MSG__DETAIL__PREVIOUS_AND_NEXT_POINT__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'previous'
// Member 'next'
#include "rosidl_runtime_c/string.h"

/// Struct defined in msg/PreviousAndNextPoint in the package robot_ros2_msgs.
typedef struct robot_ros2_msgs__msg__PreviousAndNextPoint
{
  rosidl_runtime_c__String previous;
  rosidl_runtime_c__String next;
} robot_ros2_msgs__msg__PreviousAndNextPoint;

// Struct for a sequence of robot_ros2_msgs__msg__PreviousAndNextPoint.
typedef struct robot_ros2_msgs__msg__PreviousAndNextPoint__Sequence
{
  robot_ros2_msgs__msg__PreviousAndNextPoint * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} robot_ros2_msgs__msg__PreviousAndNextPoint__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // ROBOT_ROS2_MSGS__MSG__DETAIL__PREVIOUS_AND_NEXT_POINT__STRUCT_H_
