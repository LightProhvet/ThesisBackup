// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from robot_ros2_msgs:msg/PreviousAndNextPoint.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "robot_ros2_msgs/msg/detail/previous_and_next_point__rosidl_typesupport_introspection_c.h"
#include "robot_ros2_msgs/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "robot_ros2_msgs/msg/detail/previous_and_next_point__functions.h"
#include "robot_ros2_msgs/msg/detail/previous_and_next_point__struct.h"


// Include directives for member types
// Member `previous`
// Member `next`
#include "rosidl_runtime_c/string_functions.h"

#ifdef __cplusplus
extern "C"
{
#endif

void robot_ros2_msgs__msg__PreviousAndNextPoint__rosidl_typesupport_introspection_c__PreviousAndNextPoint_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  robot_ros2_msgs__msg__PreviousAndNextPoint__init(message_memory);
}

void robot_ros2_msgs__msg__PreviousAndNextPoint__rosidl_typesupport_introspection_c__PreviousAndNextPoint_fini_function(void * message_memory)
{
  robot_ros2_msgs__msg__PreviousAndNextPoint__fini(message_memory);
}

static rosidl_typesupport_introspection_c__MessageMember robot_ros2_msgs__msg__PreviousAndNextPoint__rosidl_typesupport_introspection_c__PreviousAndNextPoint_message_member_array[2] = {
  {
    "previous",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(robot_ros2_msgs__msg__PreviousAndNextPoint, previous),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "next",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(robot_ros2_msgs__msg__PreviousAndNextPoint, next),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers robot_ros2_msgs__msg__PreviousAndNextPoint__rosidl_typesupport_introspection_c__PreviousAndNextPoint_message_members = {
  "robot_ros2_msgs__msg",  // message namespace
  "PreviousAndNextPoint",  // message name
  2,  // number of fields
  sizeof(robot_ros2_msgs__msg__PreviousAndNextPoint),
  robot_ros2_msgs__msg__PreviousAndNextPoint__rosidl_typesupport_introspection_c__PreviousAndNextPoint_message_member_array,  // message members
  robot_ros2_msgs__msg__PreviousAndNextPoint__rosidl_typesupport_introspection_c__PreviousAndNextPoint_init_function,  // function to initialize message memory (memory has to be allocated)
  robot_ros2_msgs__msg__PreviousAndNextPoint__rosidl_typesupport_introspection_c__PreviousAndNextPoint_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t robot_ros2_msgs__msg__PreviousAndNextPoint__rosidl_typesupport_introspection_c__PreviousAndNextPoint_message_type_support_handle = {
  0,
  &robot_ros2_msgs__msg__PreviousAndNextPoint__rosidl_typesupport_introspection_c__PreviousAndNextPoint_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_robot_ros2_msgs
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, robot_ros2_msgs, msg, PreviousAndNextPoint)() {
  if (!robot_ros2_msgs__msg__PreviousAndNextPoint__rosidl_typesupport_introspection_c__PreviousAndNextPoint_message_type_support_handle.typesupport_identifier) {
    robot_ros2_msgs__msg__PreviousAndNextPoint__rosidl_typesupport_introspection_c__PreviousAndNextPoint_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &robot_ros2_msgs__msg__PreviousAndNextPoint__rosidl_typesupport_introspection_c__PreviousAndNextPoint_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif
