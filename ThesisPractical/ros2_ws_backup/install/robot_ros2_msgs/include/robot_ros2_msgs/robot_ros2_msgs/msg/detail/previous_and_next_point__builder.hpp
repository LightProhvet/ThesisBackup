// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from robot_ros2_msgs:msg/PreviousAndNextPoint.idl
// generated code does not contain a copyright notice

#ifndef ROBOT_ROS2_MSGS__MSG__DETAIL__PREVIOUS_AND_NEXT_POINT__BUILDER_HPP_
#define ROBOT_ROS2_MSGS__MSG__DETAIL__PREVIOUS_AND_NEXT_POINT__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "robot_ros2_msgs/msg/detail/previous_and_next_point__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace robot_ros2_msgs
{

namespace msg
{

namespace builder
{

class Init_PreviousAndNextPoint_next
{
public:
  explicit Init_PreviousAndNextPoint_next(::robot_ros2_msgs::msg::PreviousAndNextPoint & msg)
  : msg_(msg)
  {}
  ::robot_ros2_msgs::msg::PreviousAndNextPoint next(::robot_ros2_msgs::msg::PreviousAndNextPoint::_next_type arg)
  {
    msg_.next = std::move(arg);
    return std::move(msg_);
  }

private:
  ::robot_ros2_msgs::msg::PreviousAndNextPoint msg_;
};

class Init_PreviousAndNextPoint_previous
{
public:
  Init_PreviousAndNextPoint_previous()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_PreviousAndNextPoint_next previous(::robot_ros2_msgs::msg::PreviousAndNextPoint::_previous_type arg)
  {
    msg_.previous = std::move(arg);
    return Init_PreviousAndNextPoint_next(msg_);
  }

private:
  ::robot_ros2_msgs::msg::PreviousAndNextPoint msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::robot_ros2_msgs::msg::PreviousAndNextPoint>()
{
  return robot_ros2_msgs::msg::builder::Init_PreviousAndNextPoint_previous();
}

}  // namespace robot_ros2_msgs

#endif  // ROBOT_ROS2_MSGS__MSG__DETAIL__PREVIOUS_AND_NEXT_POINT__BUILDER_HPP_
