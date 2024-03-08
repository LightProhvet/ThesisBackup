// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from robot_ros2_msgs:msg/Tag.idl
// generated code does not contain a copyright notice

#ifndef ROBOT_ROS2_MSGS__MSG__DETAIL__TAG__BUILDER_HPP_
#define ROBOT_ROS2_MSGS__MSG__DETAIL__TAG__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "robot_ros2_msgs/msg/detail/tag__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace robot_ros2_msgs
{

namespace msg
{

namespace builder
{

class Init_Tag_id
{
public:
  explicit Init_Tag_id(::robot_ros2_msgs::msg::Tag & msg)
  : msg_(msg)
  {}
  ::robot_ros2_msgs::msg::Tag id(::robot_ros2_msgs::msg::Tag::_id_type arg)
  {
    msg_.id = std::move(arg);
    return std::move(msg_);
  }

private:
  ::robot_ros2_msgs::msg::Tag msg_;
};

class Init_Tag_floor
{
public:
  explicit Init_Tag_floor(::robot_ros2_msgs::msg::Tag & msg)
  : msg_(msg)
  {}
  Init_Tag_id floor(::robot_ros2_msgs::msg::Tag::_floor_type arg)
  {
    msg_.floor = std::move(arg);
    return Init_Tag_id(msg_);
  }

private:
  ::robot_ros2_msgs::msg::Tag msg_;
};

class Init_Tag_pose
{
public:
  explicit Init_Tag_pose(::robot_ros2_msgs::msg::Tag & msg)
  : msg_(msg)
  {}
  Init_Tag_floor pose(::robot_ros2_msgs::msg::Tag::_pose_type arg)
  {
    msg_.pose = std::move(arg);
    return Init_Tag_floor(msg_);
  }

private:
  ::robot_ros2_msgs::msg::Tag msg_;
};

class Init_Tag_distance
{
public:
  explicit Init_Tag_distance(::robot_ros2_msgs::msg::Tag & msg)
  : msg_(msg)
  {}
  Init_Tag_pose distance(::robot_ros2_msgs::msg::Tag::_distance_type arg)
  {
    msg_.distance = std::move(arg);
    return Init_Tag_pose(msg_);
  }

private:
  ::robot_ros2_msgs::msg::Tag msg_;
};

class Init_Tag_header
{
public:
  Init_Tag_header()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_Tag_distance header(::robot_ros2_msgs::msg::Tag::_header_type arg)
  {
    msg_.header = std::move(arg);
    return Init_Tag_distance(msg_);
  }

private:
  ::robot_ros2_msgs::msg::Tag msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::robot_ros2_msgs::msg::Tag>()
{
  return robot_ros2_msgs::msg::builder::Init_Tag_header();
}

}  // namespace robot_ros2_msgs

#endif  // ROBOT_ROS2_MSGS__MSG__DETAIL__TAG__BUILDER_HPP_
