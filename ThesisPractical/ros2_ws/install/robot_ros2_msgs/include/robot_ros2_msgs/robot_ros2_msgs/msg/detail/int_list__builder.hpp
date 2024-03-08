// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from robot_ros2_msgs:msg/IntList.idl
// generated code does not contain a copyright notice

#ifndef ROBOT_ROS2_MSGS__MSG__DETAIL__INT_LIST__BUILDER_HPP_
#define ROBOT_ROS2_MSGS__MSG__DETAIL__INT_LIST__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "robot_ros2_msgs/msg/detail/int_list__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace robot_ros2_msgs
{

namespace msg
{

namespace builder
{

class Init_IntList_data
{
public:
  Init_IntList_data()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::robot_ros2_msgs::msg::IntList data(::robot_ros2_msgs::msg::IntList::_data_type arg)
  {
    msg_.data = std::move(arg);
    return std::move(msg_);
  }

private:
  ::robot_ros2_msgs::msg::IntList msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::robot_ros2_msgs::msg::IntList>()
{
  return robot_ros2_msgs::msg::builder::Init_IntList_data();
}

}  // namespace robot_ros2_msgs

#endif  // ROBOT_ROS2_MSGS__MSG__DETAIL__INT_LIST__BUILDER_HPP_
