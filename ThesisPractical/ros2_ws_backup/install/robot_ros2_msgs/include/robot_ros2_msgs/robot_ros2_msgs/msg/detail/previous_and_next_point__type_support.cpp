// generated from rosidl_typesupport_introspection_cpp/resource/idl__type_support.cpp.em
// with input from robot_ros2_msgs:msg/PreviousAndNextPoint.idl
// generated code does not contain a copyright notice

#include "array"
#include "cstddef"
#include "string"
#include "vector"
#include "rosidl_runtime_c/message_type_support_struct.h"
#include "rosidl_typesupport_cpp/message_type_support.hpp"
#include "rosidl_typesupport_interface/macros.h"
#include "robot_ros2_msgs/msg/detail/previous_and_next_point__struct.hpp"
#include "rosidl_typesupport_introspection_cpp/field_types.hpp"
#include "rosidl_typesupport_introspection_cpp/identifier.hpp"
#include "rosidl_typesupport_introspection_cpp/message_introspection.hpp"
#include "rosidl_typesupport_introspection_cpp/message_type_support_decl.hpp"
#include "rosidl_typesupport_introspection_cpp/visibility_control.h"

namespace robot_ros2_msgs
{

namespace msg
{

namespace rosidl_typesupport_introspection_cpp
{

void PreviousAndNextPoint_init_function(
  void * message_memory, rosidl_runtime_cpp::MessageInitialization _init)
{
  new (message_memory) robot_ros2_msgs::msg::PreviousAndNextPoint(_init);
}

void PreviousAndNextPoint_fini_function(void * message_memory)
{
  auto typed_message = static_cast<robot_ros2_msgs::msg::PreviousAndNextPoint *>(message_memory);
  typed_message->~PreviousAndNextPoint();
}

static const ::rosidl_typesupport_introspection_cpp::MessageMember PreviousAndNextPoint_message_member_array[2] = {
  {
    "previous",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(robot_ros2_msgs::msg::PreviousAndNextPoint, previous),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  },
  {
    "next",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(robot_ros2_msgs::msg::PreviousAndNextPoint, next),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  }
};

static const ::rosidl_typesupport_introspection_cpp::MessageMembers PreviousAndNextPoint_message_members = {
  "robot_ros2_msgs::msg",  // message namespace
  "PreviousAndNextPoint",  // message name
  2,  // number of fields
  sizeof(robot_ros2_msgs::msg::PreviousAndNextPoint),
  PreviousAndNextPoint_message_member_array,  // message members
  PreviousAndNextPoint_init_function,  // function to initialize message memory (memory has to be allocated)
  PreviousAndNextPoint_fini_function  // function to terminate message instance (will not free memory)
};

static const rosidl_message_type_support_t PreviousAndNextPoint_message_type_support_handle = {
  ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  &PreviousAndNextPoint_message_members,
  get_message_typesupport_handle_function,
};

}  // namespace rosidl_typesupport_introspection_cpp

}  // namespace msg

}  // namespace robot_ros2_msgs


namespace rosidl_typesupport_introspection_cpp
{

template<>
ROSIDL_TYPESUPPORT_INTROSPECTION_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<robot_ros2_msgs::msg::PreviousAndNextPoint>()
{
  return &::robot_ros2_msgs::msg::rosidl_typesupport_introspection_cpp::PreviousAndNextPoint_message_type_support_handle;
}

}  // namespace rosidl_typesupport_introspection_cpp

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_INTROSPECTION_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, robot_ros2_msgs, msg, PreviousAndNextPoint)() {
  return &::robot_ros2_msgs::msg::rosidl_typesupport_introspection_cpp::PreviousAndNextPoint_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif
