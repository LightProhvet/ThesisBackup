// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from robot_ros2_msgs:msg/IntList.idl
// generated code does not contain a copyright notice

#ifndef ROBOT_ROS2_MSGS__MSG__DETAIL__INT_LIST__TRAITS_HPP_
#define ROBOT_ROS2_MSGS__MSG__DETAIL__INT_LIST__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "robot_ros2_msgs/msg/detail/int_list__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace robot_ros2_msgs
{

namespace msg
{

inline void to_flow_style_yaml(
  const IntList & msg,
  std::ostream & out)
{
  out << "{";
  // member: data
  {
    if (msg.data.size() == 0) {
      out << "data: []";
    } else {
      out << "data: [";
      size_t pending_items = msg.data.size();
      for (auto item : msg.data) {
        rosidl_generator_traits::value_to_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const IntList & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: data
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.data.size() == 0) {
      out << "data: []\n";
    } else {
      out << "data:\n";
      for (auto item : msg.data) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "- ";
        rosidl_generator_traits::value_to_yaml(item, out);
        out << "\n";
      }
    }
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const IntList & msg, bool use_flow_style = false)
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
  const robot_ros2_msgs::msg::IntList & msg,
  std::ostream & out, size_t indentation = 0)
{
  robot_ros2_msgs::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use robot_ros2_msgs::msg::to_yaml() instead")]]
inline std::string to_yaml(const robot_ros2_msgs::msg::IntList & msg)
{
  return robot_ros2_msgs::msg::to_yaml(msg);
}

template<>
inline const char * data_type<robot_ros2_msgs::msg::IntList>()
{
  return "robot_ros2_msgs::msg::IntList";
}

template<>
inline const char * name<robot_ros2_msgs::msg::IntList>()
{
  return "robot_ros2_msgs/msg/IntList";
}

template<>
struct has_fixed_size<robot_ros2_msgs::msg::IntList>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<robot_ros2_msgs::msg::IntList>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<robot_ros2_msgs::msg::IntList>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // ROBOT_ROS2_MSGS__MSG__DETAIL__INT_LIST__TRAITS_HPP_
