// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from robot_ros2_msgs:msg/Tag.idl
// generated code does not contain a copyright notice
#include "robot_ros2_msgs/msg/detail/tag__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `header`
#include "std_msgs/msg/detail/header__functions.h"
// Member `pose`
#include "geometry_msgs/msg/detail/pose__functions.h"

bool
robot_ros2_msgs__msg__Tag__init(robot_ros2_msgs__msg__Tag * msg)
{
  if (!msg) {
    return false;
  }
  // header
  if (!std_msgs__msg__Header__init(&msg->header)) {
    robot_ros2_msgs__msg__Tag__fini(msg);
    return false;
  }
  // distance
  // pose
  if (!geometry_msgs__msg__Pose__init(&msg->pose)) {
    robot_ros2_msgs__msg__Tag__fini(msg);
    return false;
  }
  // floor
  // id
  return true;
}

void
robot_ros2_msgs__msg__Tag__fini(robot_ros2_msgs__msg__Tag * msg)
{
  if (!msg) {
    return;
  }
  // header
  std_msgs__msg__Header__fini(&msg->header);
  // distance
  // pose
  geometry_msgs__msg__Pose__fini(&msg->pose);
  // floor
  // id
}

bool
robot_ros2_msgs__msg__Tag__are_equal(const robot_ros2_msgs__msg__Tag * lhs, const robot_ros2_msgs__msg__Tag * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // header
  if (!std_msgs__msg__Header__are_equal(
      &(lhs->header), &(rhs->header)))
  {
    return false;
  }
  // distance
  if (lhs->distance != rhs->distance) {
    return false;
  }
  // pose
  if (!geometry_msgs__msg__Pose__are_equal(
      &(lhs->pose), &(rhs->pose)))
  {
    return false;
  }
  // floor
  if (lhs->floor != rhs->floor) {
    return false;
  }
  // id
  if (lhs->id != rhs->id) {
    return false;
  }
  return true;
}

bool
robot_ros2_msgs__msg__Tag__copy(
  const robot_ros2_msgs__msg__Tag * input,
  robot_ros2_msgs__msg__Tag * output)
{
  if (!input || !output) {
    return false;
  }
  // header
  if (!std_msgs__msg__Header__copy(
      &(input->header), &(output->header)))
  {
    return false;
  }
  // distance
  output->distance = input->distance;
  // pose
  if (!geometry_msgs__msg__Pose__copy(
      &(input->pose), &(output->pose)))
  {
    return false;
  }
  // floor
  output->floor = input->floor;
  // id
  output->id = input->id;
  return true;
}

robot_ros2_msgs__msg__Tag *
robot_ros2_msgs__msg__Tag__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  robot_ros2_msgs__msg__Tag * msg = (robot_ros2_msgs__msg__Tag *)allocator.allocate(sizeof(robot_ros2_msgs__msg__Tag), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(robot_ros2_msgs__msg__Tag));
  bool success = robot_ros2_msgs__msg__Tag__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
robot_ros2_msgs__msg__Tag__destroy(robot_ros2_msgs__msg__Tag * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    robot_ros2_msgs__msg__Tag__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
robot_ros2_msgs__msg__Tag__Sequence__init(robot_ros2_msgs__msg__Tag__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  robot_ros2_msgs__msg__Tag * data = NULL;

  if (size) {
    data = (robot_ros2_msgs__msg__Tag *)allocator.zero_allocate(size, sizeof(robot_ros2_msgs__msg__Tag), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = robot_ros2_msgs__msg__Tag__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        robot_ros2_msgs__msg__Tag__fini(&data[i - 1]);
      }
      allocator.deallocate(data, allocator.state);
      return false;
    }
  }
  array->data = data;
  array->size = size;
  array->capacity = size;
  return true;
}

void
robot_ros2_msgs__msg__Tag__Sequence__fini(robot_ros2_msgs__msg__Tag__Sequence * array)
{
  if (!array) {
    return;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();

  if (array->data) {
    // ensure that data and capacity values are consistent
    assert(array->capacity > 0);
    // finalize all array elements
    for (size_t i = 0; i < array->capacity; ++i) {
      robot_ros2_msgs__msg__Tag__fini(&array->data[i]);
    }
    allocator.deallocate(array->data, allocator.state);
    array->data = NULL;
    array->size = 0;
    array->capacity = 0;
  } else {
    // ensure that data, size, and capacity values are consistent
    assert(0 == array->size);
    assert(0 == array->capacity);
  }
}

robot_ros2_msgs__msg__Tag__Sequence *
robot_ros2_msgs__msg__Tag__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  robot_ros2_msgs__msg__Tag__Sequence * array = (robot_ros2_msgs__msg__Tag__Sequence *)allocator.allocate(sizeof(robot_ros2_msgs__msg__Tag__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = robot_ros2_msgs__msg__Tag__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
robot_ros2_msgs__msg__Tag__Sequence__destroy(robot_ros2_msgs__msg__Tag__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    robot_ros2_msgs__msg__Tag__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
robot_ros2_msgs__msg__Tag__Sequence__are_equal(const robot_ros2_msgs__msg__Tag__Sequence * lhs, const robot_ros2_msgs__msg__Tag__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!robot_ros2_msgs__msg__Tag__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
robot_ros2_msgs__msg__Tag__Sequence__copy(
  const robot_ros2_msgs__msg__Tag__Sequence * input,
  robot_ros2_msgs__msg__Tag__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(robot_ros2_msgs__msg__Tag);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    robot_ros2_msgs__msg__Tag * data =
      (robot_ros2_msgs__msg__Tag *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!robot_ros2_msgs__msg__Tag__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          robot_ros2_msgs__msg__Tag__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!robot_ros2_msgs__msg__Tag__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
