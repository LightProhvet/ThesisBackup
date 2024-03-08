// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from robot_ros2_msgs:msg/PreviousAndNextPoint.idl
// generated code does not contain a copyright notice

#ifndef ROBOT_ROS2_MSGS__MSG__DETAIL__PREVIOUS_AND_NEXT_POINT__TRAITS_HPP_
#define ROBOT_ROS2_MSGS__MSG__DETAIL__PREVIOUS_AND_NEXT_POINT__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "robot_ros2_msgs/msg/detail/previous_and_next_point__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace robot_ros2_msgs
{

namespace msg
{

inline void to_flow_style_yaml(
  const PreviousAndNextPoint & msg,
  std::ostream & out)
{
  out << "{";
  // member: previous
  {
    out << "previous: ";
    rosidl_generator_traits::value_to_yaml(msg.previous, out);
    out << ", ";
  }

  // member: next
  {
    out << "next: ";
    rosidl_generator_traits::value_to_yaml(msg.next, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const PreviousAndNextPoint & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: previous
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "previous: ";
    rosidl_generator_traits::value_to_yaml(msg.previous, out);
    out << "\n";
  }

  // member: next
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "next: ";
    rosidl_generator_traits::value_to_yaml(msg.next, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const PreviousAndNextPoint & msg, bool use_flow_style = false)
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
  const robot_ros2_msgs::msg::PreviousAndNextPoint & msg,
  std::ostream & out, size_t indentation = 0)
{
  robot_ros2_msgs::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use robot_ros2_msgs::msg::to_yaml() instead")]]
inline std::string to_yaml(const robot_ros2_msgs::msg::PreviousAndNextPoint & msg)
{
  return robot_ros2_msgs::msg::to_yaml(msg);
}

template<>
inline const char * data_type<robot_ros2_msgs::msg::PreviousAndNextPoint>()
{
  return "robot_ros2_msgs::msg::PreviousAndNextPoint";
}

template<>
inline const char * name<robot_ros2_msgs::msg::PreviousAndNextPoint>()
{
  return "robot_ros2_msgs/msg/PreviousAndNextPoint";
}

template<>
struct has_fixed_size<robot_ros2_msgs::msg::PreviousAndNextPoint>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<robot_ros2_msgs::msg::PreviousAndNextPoint>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<robot_ros2_msgs::msg::PreviousAndNextPoint>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // ROBOT_ROS2_MSGS__MSG__DETAIL__PREVIOUS_AND_NEXT_POINT__TRAITS_HPP_
