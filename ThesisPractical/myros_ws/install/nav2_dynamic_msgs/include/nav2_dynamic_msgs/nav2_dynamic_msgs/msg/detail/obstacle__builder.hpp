// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from nav2_dynamic_msgs:msg/Obstacle.idl
// generated code does not contain a copyright notice

#ifndef NAV2_DYNAMIC_MSGS__MSG__DETAIL__OBSTACLE__BUILDER_HPP_
#define NAV2_DYNAMIC_MSGS__MSG__DETAIL__OBSTACLE__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "nav2_dynamic_msgs/msg/detail/obstacle__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace nav2_dynamic_msgs
{

namespace msg
{

namespace builder
{

class Init_Obstacle_size
{
public:
  explicit Init_Obstacle_size(::nav2_dynamic_msgs::msg::Obstacle & msg)
  : msg_(msg)
  {}
  ::nav2_dynamic_msgs::msg::Obstacle size(::nav2_dynamic_msgs::msg::Obstacle::_size_type arg)
  {
    msg_.size = std::move(arg);
    return std::move(msg_);
  }

private:
  ::nav2_dynamic_msgs::msg::Obstacle msg_;
};

class Init_Obstacle_velocity
{
public:
  explicit Init_Obstacle_velocity(::nav2_dynamic_msgs::msg::Obstacle & msg)
  : msg_(msg)
  {}
  Init_Obstacle_size velocity(::nav2_dynamic_msgs::msg::Obstacle::_velocity_type arg)
  {
    msg_.velocity = std::move(arg);
    return Init_Obstacle_size(msg_);
  }

private:
  ::nav2_dynamic_msgs::msg::Obstacle msg_;
};

class Init_Obstacle_position
{
public:
  explicit Init_Obstacle_position(::nav2_dynamic_msgs::msg::Obstacle & msg)
  : msg_(msg)
  {}
  Init_Obstacle_velocity position(::nav2_dynamic_msgs::msg::Obstacle::_position_type arg)
  {
    msg_.position = std::move(arg);
    return Init_Obstacle_velocity(msg_);
  }

private:
  ::nav2_dynamic_msgs::msg::Obstacle msg_;
};

class Init_Obstacle_score
{
public:
  explicit Init_Obstacle_score(::nav2_dynamic_msgs::msg::Obstacle & msg)
  : msg_(msg)
  {}
  Init_Obstacle_position score(::nav2_dynamic_msgs::msg::Obstacle::_score_type arg)
  {
    msg_.score = std::move(arg);
    return Init_Obstacle_position(msg_);
  }

private:
  ::nav2_dynamic_msgs::msg::Obstacle msg_;
};

class Init_Obstacle_uuid
{
public:
  Init_Obstacle_uuid()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_Obstacle_score uuid(::nav2_dynamic_msgs::msg::Obstacle::_uuid_type arg)
  {
    msg_.uuid = std::move(arg);
    return Init_Obstacle_score(msg_);
  }

private:
  ::nav2_dynamic_msgs::msg::Obstacle msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::nav2_dynamic_msgs::msg::Obstacle>()
{
  return nav2_dynamic_msgs::msg::builder::Init_Obstacle_uuid();
}

}  // namespace nav2_dynamic_msgs

#endif  // NAV2_DYNAMIC_MSGS__MSG__DETAIL__OBSTACLE__BUILDER_HPP_