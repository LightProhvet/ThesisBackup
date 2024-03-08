// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from robot_ros2_msgs:msg/Tag.idl
// generated code does not contain a copyright notice

#ifndef ROBOT_ROS2_MSGS__MSG__DETAIL__TAG__STRUCT_HPP_
#define ROBOT_ROS2_MSGS__MSG__DETAIL__TAG__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


// Include directives for member types
// Member 'header'
#include "std_msgs/msg/detail/header__struct.hpp"
// Member 'pose'
#include "geometry_msgs/msg/detail/pose__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__robot_ros2_msgs__msg__Tag __attribute__((deprecated))
#else
# define DEPRECATED__robot_ros2_msgs__msg__Tag __declspec(deprecated)
#endif

namespace robot_ros2_msgs
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct Tag_
{
  using Type = Tag_<ContainerAllocator>;

  explicit Tag_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : header(_init),
    pose(_init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->distance = 0.0f;
      this->floor = 0;
      this->id = 0;
    }
  }

  explicit Tag_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : header(_alloc, _init),
    pose(_alloc, _init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->distance = 0.0f;
      this->floor = 0;
      this->id = 0;
    }
  }

  // field types and members
  using _header_type =
    std_msgs::msg::Header_<ContainerAllocator>;
  _header_type header;
  using _distance_type =
    float;
  _distance_type distance;
  using _pose_type =
    geometry_msgs::msg::Pose_<ContainerAllocator>;
  _pose_type pose;
  using _floor_type =
    int16_t;
  _floor_type floor;
  using _id_type =
    int16_t;
  _id_type id;

  // setters for named parameter idiom
  Type & set__header(
    const std_msgs::msg::Header_<ContainerAllocator> & _arg)
  {
    this->header = _arg;
    return *this;
  }
  Type & set__distance(
    const float & _arg)
  {
    this->distance = _arg;
    return *this;
  }
  Type & set__pose(
    const geometry_msgs::msg::Pose_<ContainerAllocator> & _arg)
  {
    this->pose = _arg;
    return *this;
  }
  Type & set__floor(
    const int16_t & _arg)
  {
    this->floor = _arg;
    return *this;
  }
  Type & set__id(
    const int16_t & _arg)
  {
    this->id = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    robot_ros2_msgs::msg::Tag_<ContainerAllocator> *;
  using ConstRawPtr =
    const robot_ros2_msgs::msg::Tag_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<robot_ros2_msgs::msg::Tag_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<robot_ros2_msgs::msg::Tag_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      robot_ros2_msgs::msg::Tag_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<robot_ros2_msgs::msg::Tag_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      robot_ros2_msgs::msg::Tag_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<robot_ros2_msgs::msg::Tag_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<robot_ros2_msgs::msg::Tag_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<robot_ros2_msgs::msg::Tag_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__robot_ros2_msgs__msg__Tag
    std::shared_ptr<robot_ros2_msgs::msg::Tag_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__robot_ros2_msgs__msg__Tag
    std::shared_ptr<robot_ros2_msgs::msg::Tag_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const Tag_ & other) const
  {
    if (this->header != other.header) {
      return false;
    }
    if (this->distance != other.distance) {
      return false;
    }
    if (this->pose != other.pose) {
      return false;
    }
    if (this->floor != other.floor) {
      return false;
    }
    if (this->id != other.id) {
      return false;
    }
    return true;
  }
  bool operator!=(const Tag_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct Tag_

// alias to use template instance with default allocator
using Tag =
  robot_ros2_msgs::msg::Tag_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace robot_ros2_msgs

#endif  // ROBOT_ROS2_MSGS__MSG__DETAIL__TAG__STRUCT_HPP_
