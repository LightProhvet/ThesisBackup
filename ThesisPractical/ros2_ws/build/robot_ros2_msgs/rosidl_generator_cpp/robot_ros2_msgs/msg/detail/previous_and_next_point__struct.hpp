// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from robot_ros2_msgs:msg/PreviousAndNextPoint.idl
// generated code does not contain a copyright notice

#ifndef ROBOT_ROS2_MSGS__MSG__DETAIL__PREVIOUS_AND_NEXT_POINT__STRUCT_HPP_
#define ROBOT_ROS2_MSGS__MSG__DETAIL__PREVIOUS_AND_NEXT_POINT__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__robot_ros2_msgs__msg__PreviousAndNextPoint __attribute__((deprecated))
#else
# define DEPRECATED__robot_ros2_msgs__msg__PreviousAndNextPoint __declspec(deprecated)
#endif

namespace robot_ros2_msgs
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct PreviousAndNextPoint_
{
  using Type = PreviousAndNextPoint_<ContainerAllocator>;

  explicit PreviousAndNextPoint_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->previous = "";
      this->next = "";
    }
  }

  explicit PreviousAndNextPoint_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : previous(_alloc),
    next(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->previous = "";
      this->next = "";
    }
  }

  // field types and members
  using _previous_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _previous_type previous;
  using _next_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _next_type next;

  // setters for named parameter idiom
  Type & set__previous(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->previous = _arg;
    return *this;
  }
  Type & set__next(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->next = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    robot_ros2_msgs::msg::PreviousAndNextPoint_<ContainerAllocator> *;
  using ConstRawPtr =
    const robot_ros2_msgs::msg::PreviousAndNextPoint_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<robot_ros2_msgs::msg::PreviousAndNextPoint_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<robot_ros2_msgs::msg::PreviousAndNextPoint_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      robot_ros2_msgs::msg::PreviousAndNextPoint_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<robot_ros2_msgs::msg::PreviousAndNextPoint_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      robot_ros2_msgs::msg::PreviousAndNextPoint_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<robot_ros2_msgs::msg::PreviousAndNextPoint_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<robot_ros2_msgs::msg::PreviousAndNextPoint_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<robot_ros2_msgs::msg::PreviousAndNextPoint_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__robot_ros2_msgs__msg__PreviousAndNextPoint
    std::shared_ptr<robot_ros2_msgs::msg::PreviousAndNextPoint_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__robot_ros2_msgs__msg__PreviousAndNextPoint
    std::shared_ptr<robot_ros2_msgs::msg::PreviousAndNextPoint_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const PreviousAndNextPoint_ & other) const
  {
    if (this->previous != other.previous) {
      return false;
    }
    if (this->next != other.next) {
      return false;
    }
    return true;
  }
  bool operator!=(const PreviousAndNextPoint_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct PreviousAndNextPoint_

// alias to use template instance with default allocator
using PreviousAndNextPoint =
  robot_ros2_msgs::msg::PreviousAndNextPoint_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace robot_ros2_msgs

#endif  // ROBOT_ROS2_MSGS__MSG__DETAIL__PREVIOUS_AND_NEXT_POINT__STRUCT_HPP_
