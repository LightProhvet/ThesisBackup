// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from robot_ros2_msgs:msg/Encoders.idl
// generated code does not contain a copyright notice

#ifndef ROBOT_ROS2_MSGS__MSG__DETAIL__ENCODERS__BUILDER_HPP_
#define ROBOT_ROS2_MSGS__MSG__DETAIL__ENCODERS__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "robot_ros2_msgs/msg/detail/encoders__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace robot_ros2_msgs
{

namespace msg
{

namespace builder
{

class Init_Encoders_right_back
{
public:
  explicit Init_Encoders_right_back(::robot_ros2_msgs::msg::Encoders & msg)
  : msg_(msg)
  {}
  ::robot_ros2_msgs::msg::Encoders right_back(::robot_ros2_msgs::msg::Encoders::_right_back_type arg)
  {
    msg_.right_back = std::move(arg);
    return std::move(msg_);
  }

private:
  ::robot_ros2_msgs::msg::Encoders msg_;
};

class Init_Encoders_left_back
{
public:
  explicit Init_Encoders_left_back(::robot_ros2_msgs::msg::Encoders & msg)
  : msg_(msg)
  {}
  Init_Encoders_right_back left_back(::robot_ros2_msgs::msg::Encoders::_left_back_type arg)
  {
    msg_.left_back = std::move(arg);
    return Init_Encoders_right_back(msg_);
  }

private:
  ::robot_ros2_msgs::msg::Encoders msg_;
};

class Init_Encoders_left_front
{
public:
  explicit Init_Encoders_left_front(::robot_ros2_msgs::msg::Encoders & msg)
  : msg_(msg)
  {}
  Init_Encoders_left_back left_front(::robot_ros2_msgs::msg::Encoders::_left_front_type arg)
  {
    msg_.left_front = std::move(arg);
    return Init_Encoders_left_back(msg_);
  }

private:
  ::robot_ros2_msgs::msg::Encoders msg_;
};

class Init_Encoders_right_front
{
public:
  explicit Init_Encoders_right_front(::robot_ros2_msgs::msg::Encoders & msg)
  : msg_(msg)
  {}
  Init_Encoders_left_front right_front(::robot_ros2_msgs::msg::Encoders::_right_front_type arg)
  {
    msg_.right_front = std::move(arg);
    return Init_Encoders_left_front(msg_);
  }

private:
  ::robot_ros2_msgs::msg::Encoders msg_;
};

class Init_Encoders_header
{
public:
  Init_Encoders_header()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_Encoders_right_front header(::robot_ros2_msgs::msg::Encoders::_header_type arg)
  {
    msg_.header = std::move(arg);
    return Init_Encoders_right_front(msg_);
  }

private:
  ::robot_ros2_msgs::msg::Encoders msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::robot_ros2_msgs::msg::Encoders>()
{
  return robot_ros2_msgs::msg::builder::Init_Encoders_header();
}

}  // namespace robot_ros2_msgs

#endif  // ROBOT_ROS2_MSGS__MSG__DETAIL__ENCODERS__BUILDER_HPP_
