// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from robot_ros2_msgs:msg/IntList.idl
// generated code does not contain a copyright notice

#ifndef ROBOT_ROS2_MSGS__MSG__DETAIL__INT_LIST__STRUCT_HPP_
#define ROBOT_ROS2_MSGS__MSG__DETAIL__INT_LIST__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__robot_ros2_msgs__msg__IntList __attribute__((deprecated))
#else
# define DEPRECATED__robot_ros2_msgs__msg__IntList __declspec(deprecated)
#endif

namespace robot_ros2_msgs
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct IntList_
{
  using Type = IntList_<ContainerAllocator>;

  explicit IntList_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_init;
  }

  explicit IntList_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_init;
    (void)_alloc;
  }

  // field types and members
  using _data_type =
    std::vector<int32_t, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<int32_t>>;
  _data_type data;

  // setters for named parameter idiom
  Type & set__data(
    const std::vector<int32_t, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<int32_t>> & _arg)
  {
    this->data = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    robot_ros2_msgs::msg::IntList_<ContainerAllocator> *;
  using ConstRawPtr =
    const robot_ros2_msgs::msg::IntList_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<robot_ros2_msgs::msg::IntList_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<robot_ros2_msgs::msg::IntList_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      robot_ros2_msgs::msg::IntList_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<robot_ros2_msgs::msg::IntList_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      robot_ros2_msgs::msg::IntList_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<robot_ros2_msgs::msg::IntList_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<robot_ros2_msgs::msg::IntList_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<robot_ros2_msgs::msg::IntList_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__robot_ros2_msgs__msg__IntList
    std::shared_ptr<robot_ros2_msgs::msg::IntList_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__robot_ros2_msgs__msg__IntList
    std::shared_ptr<robot_ros2_msgs::msg::IntList_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const IntList_ & other) const
  {
    if (this->data != other.data) {
      return false;
    }
    return true;
  }
  bool operator!=(const IntList_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct IntList_

// alias to use template instance with default allocator
using IntList =
  robot_ros2_msgs::msg::IntList_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace robot_ros2_msgs

#endif  // ROBOT_ROS2_MSGS__MSG__DETAIL__INT_LIST__STRUCT_HPP_
