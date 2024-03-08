// generated from rosidl_generator_c/resource/idl__functions.h.em
// with input from robot_ros2_msgs:msg/Encoders.idl
// generated code does not contain a copyright notice

#ifndef ROBOT_ROS2_MSGS__MSG__DETAIL__ENCODERS__FUNCTIONS_H_
#define ROBOT_ROS2_MSGS__MSG__DETAIL__ENCODERS__FUNCTIONS_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stdlib.h>

#include "rosidl_runtime_c/visibility_control.h"
#include "robot_ros2_msgs/msg/rosidl_generator_c__visibility_control.h"

#include "robot_ros2_msgs/msg/detail/encoders__struct.h"

/// Initialize msg/Encoders message.
/**
 * If the init function is called twice for the same message without
 * calling fini inbetween previously allocated memory will be leaked.
 * \param[in,out] msg The previously allocated message pointer.
 * Fields without a default value will not be initialized by this function.
 * You might want to call memset(msg, 0, sizeof(
 * robot_ros2_msgs__msg__Encoders
 * )) before or use
 * robot_ros2_msgs__msg__Encoders__create()
 * to allocate and initialize the message.
 * \return true if initialization was successful, otherwise false
 */
ROSIDL_GENERATOR_C_PUBLIC_robot_ros2_msgs
bool
robot_ros2_msgs__msg__Encoders__init(robot_ros2_msgs__msg__Encoders * msg);

/// Finalize msg/Encoders message.
/**
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_robot_ros2_msgs
void
robot_ros2_msgs__msg__Encoders__fini(robot_ros2_msgs__msg__Encoders * msg);

/// Create msg/Encoders message.
/**
 * It allocates the memory for the message, sets the memory to zero, and
 * calls
 * robot_ros2_msgs__msg__Encoders__init().
 * \return The pointer to the initialized message if successful,
 * otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_robot_ros2_msgs
robot_ros2_msgs__msg__Encoders *
robot_ros2_msgs__msg__Encoders__create();

/// Destroy msg/Encoders message.
/**
 * It calls
 * robot_ros2_msgs__msg__Encoders__fini()
 * and frees the memory of the message.
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_robot_ros2_msgs
void
robot_ros2_msgs__msg__Encoders__destroy(robot_ros2_msgs__msg__Encoders * msg);

/// Check for msg/Encoders message equality.
/**
 * \param[in] lhs The message on the left hand size of the equality operator.
 * \param[in] rhs The message on the right hand size of the equality operator.
 * \return true if messages are equal, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_robot_ros2_msgs
bool
robot_ros2_msgs__msg__Encoders__are_equal(const robot_ros2_msgs__msg__Encoders * lhs, const robot_ros2_msgs__msg__Encoders * rhs);

/// Copy a msg/Encoders message.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source message pointer.
 * \param[out] output The target message pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer is null
 *   or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_robot_ros2_msgs
bool
robot_ros2_msgs__msg__Encoders__copy(
  const robot_ros2_msgs__msg__Encoders * input,
  robot_ros2_msgs__msg__Encoders * output);

/// Initialize array of msg/Encoders messages.
/**
 * It allocates the memory for the number of elements and calls
 * robot_ros2_msgs__msg__Encoders__init()
 * for each element of the array.
 * \param[in,out] array The allocated array pointer.
 * \param[in] size The size / capacity of the array.
 * \return true if initialization was successful, otherwise false
 * If the array pointer is valid and the size is zero it is guaranteed
 # to return true.
 */
ROSIDL_GENERATOR_C_PUBLIC_robot_ros2_msgs
bool
robot_ros2_msgs__msg__Encoders__Sequence__init(robot_ros2_msgs__msg__Encoders__Sequence * array, size_t size);

/// Finalize array of msg/Encoders messages.
/**
 * It calls
 * robot_ros2_msgs__msg__Encoders__fini()
 * for each element of the array and frees the memory for the number of
 * elements.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_robot_ros2_msgs
void
robot_ros2_msgs__msg__Encoders__Sequence__fini(robot_ros2_msgs__msg__Encoders__Sequence * array);

/// Create array of msg/Encoders messages.
/**
 * It allocates the memory for the array and calls
 * robot_ros2_msgs__msg__Encoders__Sequence__init().
 * \param[in] size The size / capacity of the array.
 * \return The pointer to the initialized array if successful, otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_robot_ros2_msgs
robot_ros2_msgs__msg__Encoders__Sequence *
robot_ros2_msgs__msg__Encoders__Sequence__create(size_t size);

/// Destroy array of msg/Encoders messages.
/**
 * It calls
 * robot_ros2_msgs__msg__Encoders__Sequence__fini()
 * on the array,
 * and frees the memory of the array.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_robot_ros2_msgs
void
robot_ros2_msgs__msg__Encoders__Sequence__destroy(robot_ros2_msgs__msg__Encoders__Sequence * array);

/// Check for msg/Encoders message array equality.
/**
 * \param[in] lhs The message array on the left hand size of the equality operator.
 * \param[in] rhs The message array on the right hand size of the equality operator.
 * \return true if message arrays are equal in size and content, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_robot_ros2_msgs
bool
robot_ros2_msgs__msg__Encoders__Sequence__are_equal(const robot_ros2_msgs__msg__Encoders__Sequence * lhs, const robot_ros2_msgs__msg__Encoders__Sequence * rhs);

/// Copy an array of msg/Encoders messages.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source array pointer.
 * \param[out] output The target array pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer
 *   is null or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_robot_ros2_msgs
bool
robot_ros2_msgs__msg__Encoders__Sequence__copy(
  const robot_ros2_msgs__msg__Encoders__Sequence * input,
  robot_ros2_msgs__msg__Encoders__Sequence * output);

#ifdef __cplusplus
}
#endif

#endif  // ROBOT_ROS2_MSGS__MSG__DETAIL__ENCODERS__FUNCTIONS_H_