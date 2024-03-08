// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from robot_ros2_msgs:msg/Encoders.idl
// generated code does not contain a copyright notice

#ifndef ROBOT_ROS2_MSGS__MSG__DETAIL__ENCODERS__STRUCT_HPP_
#define ROBOT_ROS2_MSGS__MSG__DETAIL__ENCODERS__STRUCT_HPP_

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

#ifndef _WIN32
# define DEPRECATED__robot_ros2_msgs__msg__Encoders __attribute__((deprecated))
#else
# define DEPRECATED__robot_ros2_msgs__msg__Encoders __declspec(deprecated)
#endif

namespace robot_ros2_msgs
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct Encoders_
{
  using Type = Encoders_<ContainerAllocator>;

  explicit Encoders_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : header(_init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->right_front = 0.0f;
      this->left_front = 0.0f;
      this->left_back = 0.0f;
      this->right_back = 0.0f;
    }
  }

  explicit Encoders_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : header(_alloc, _init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->right_front = 0.0f;
      this->left_front = 0.0f;
      this->left_back = 0.0f;
      this->right_back = 0.0f;
    }
  }

  // field types and members
  using _header_type =
    std_msgs::msg::Header_<ContainerAllocator>;
  _header_type header;
  using _right_front_type =
    float;
  _right_front_type right_front;
  using _left_front_type =
    float;
  _left_front_type left_front;
  using _left_back_type =
    float;
  _left_back_type left_back;
  using _right_back_type =
    float;
  _right_back_type right_back;

  // setters for named parameter idiom
  Type & set__header(
    const std_msgs::msg::Header_<ContainerAllocator> & _arg)
  {
    this->header = _arg;
    return *this;
  }
  Type & set__right_front(
    const float & _arg)
  {
    this->right_front = _arg;
    return *this;
  }
  Type & set__left_front(
    const float & _arg)
  {
    this->left_front = _arg;
    return *this;
  }
  Type & set__left_back(
    const float & _arg)
  {
    this->left_back = _arg;
    return *this;
  }
  Type & set__right_back(
    const float & _arg)
  {
    this->right_back = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    robot_ros2_msgs::msg::Encoders_<ContainerAllocator> *;
  using ConstRawPtr =
    const robot_ros2_msgs::msg::Encoders_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<robot_ros2_msgs::msg::Encoders_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<robot_ros2_msgs::msg::Encoders_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      robot_ros2_msgs::msg::Encoders_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<robot_ros2_msgs::msg::Encoders_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      robot_ros2_msgs::msg::Encoders_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<robot_ros2_msgs::msg::Encoders_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<robot_ros2_msgs::msg::Encoders_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<robot_ros2_msgs::msg::Encoders_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__robot_ros2_msgs__msg__Encoders
    std::shared_ptr<robot_ros2_msgs::msg::Encoders_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__robot_ros2_msgs__msg__Encoders
    std::shared_ptr<robot_ros2_msgs::msg::Encoders_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const Encoders_ & other) const
  {
    if (this->header != other.header) {
      return false;
    }
    if (this->right_front != other.right_front) {
      return false;
    }
    if (this->left_front != other.left_front) {
      return false;
    }
    if (this->left_back != other.left_back) {
      return false;
    }
    if (this->right_back != other.right_back) {
      return false;
    }
    return true;
  }
  bool operator!=(const Encoders_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct Encoders_

// alias to use template instance with default allocator
using Encoders =
  robot_ros2_msgs::msg::Encoders_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace robot_ros2_msgs

#endif  // ROBOT_ROS2_MSGS__MSG__DETAIL__ENCODERS__STRUCT_HPP_
