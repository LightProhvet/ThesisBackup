// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from robot_ros2_msgs:msg/Encoders.idl
// generated code does not contain a copyright notice

#ifndef ROBOT_ROS2_MSGS__MSG__DETAIL__ENCODERS__TRAITS_HPP_
#define ROBOT_ROS2_MSGS__MSG__DETAIL__ENCODERS__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "robot_ros2_msgs/msg/detail/encoders__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

// Include directives for member types
// Member 'header'
#include "std_msgs/msg/detail/header__traits.hpp"

namespace robot_ros2_msgs
{

namespace msg
{

inline void to_flow_style_yaml(
  const Encoders & msg,
  std::ostream & out)
{
  out << "{";
  // member: header
  {
    out << "header: ";
    to_flow_style_yaml(msg.header, out);
    out << ", ";
  }

  // member: right_front
  {
    out << "right_front: ";
    rosidl_generator_traits::value_to_yaml(msg.right_front, out);
    out << ", ";
  }

  // member: left_front
  {
    out << "left_front: ";
    rosidl_generator_traits::value_to_yaml(msg.left_front, out);
    out << ", ";
  }

  // member: left_back
  {
    out << "left_back: ";
    rosidl_generator_traits::value_to_yaml(msg.left_back, out);
    out << ", ";
  }

  // member: right_back
  {
    out << "right_back: ";
    rosidl_generator_traits::value_to_yaml(msg.right_back, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const Encoders & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: header
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "header:\n";
    to_block_style_yaml(msg.header, out, indentation + 2);
  }

  // member: right_front
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "right_front: ";
    rosidl_generator_traits::value_to_yaml(msg.right_front, out);
    out << "\n";
  }

  // member: left_front
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "left_front: ";
    rosidl_generator_traits::value_to_yaml(msg.left_front, out);
    out << "\n";
  }

  // member: left_back
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "left_back: ";
    rosidl_generator_traits::value_to_yaml(msg.left_back, out);
    out << "\n";
  }

  // member: right_back
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "right_back: ";
    rosidl_generator_traits::value_to_yaml(msg.right_back, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const Encoders & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace msg

}  // namespace robot_ros2_msgs

namespace rosidl_generator_traits
{

[[deprecated("use robot_ros2_msgs::msg::to_block_style_yaml() instead")]]
inline void to_yaml(
  const robot_ros2_msgs::msg::Encoders & msg,
  std::ostream & out, size_t indentation = 0)
{
  robot_ros2_msgs::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use robot_ros2_msgs::msg::to_yaml() instead")]]
inline std::string to_yaml(const robot_ros2_msgs::msg::Encoders & msg)
{
  return robot_ros2_msgs::msg::to_yaml(msg);
}

template<>
inline const char * data_type<robot_ros2_msgs::msg::Encoders>()
{
  return "robot_ros2_msgs::msg::Encoders";
}

template<>
inline const char * name<robot_ros2_msgs::msg::Encoders>()
{
  return "robot_ros2_msgs/msg/Encoders";
}

template<>
struct has_fixed_size<robot_ros2_msgs::msg::Encoders>
  : std::integral_constant<bool, has_fixed_size<std_msgs::msg::Header>::value> {};

template<>
struct has_bounded_size<robot_ros2_msgs::msg::Encoders>
  : std::integral_constant<bool, has_bounded_size<std_msgs::msg::Header>::value> {};

template<>
struct is_message<robot_ros2_msgs::msg::Encoders>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // ROBOT_ROS2_MSGS__MSG__DETAIL__ENCODERS__TRAITS_HPP_
