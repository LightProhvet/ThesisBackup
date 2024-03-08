// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from robot_ros2_msgs:msg/IntList.idl
// generated code does not contain a copyright notice
#include "robot_ros2_msgs/msg/detail/int_list__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `data`
#include "rosidl_runtime_c/primitives_sequence_functions.h"

bool
robot_ros2_msgs__msg__IntList__init(robot_ros2_msgs__msg__IntList * msg)
{
  if (!msg) {
    return false;
  }
  // data
  if (!rosidl_runtime_c__int32__Sequence__init(&msg->data, 0)) {
    robot_ros2_msgs__msg__IntList__fini(msg);
    return false;
  }
  return true;
}

void
robot_ros2_msgs__msg__IntList__fini(robot_ros2_msgs__msg__IntList * msg)
{
  if (!msg) {
    return;
  }
  // data
  rosidl_runtime_c__int32__Sequence__fini(&msg->data);
}

bool
robot_ros2_msgs__msg__IntList__are_equal(const robot_ros2_msgs__msg__IntList * lhs, const robot_ros2_msgs__msg__IntList * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // data
  if (!rosidl_runtime_c__int32__Sequence__are_equal(
      &(lhs->data), &(rhs->data)))
  {
    return false;
  }
  return true;
}

bool
robot_ros2_msgs__msg__IntList__copy(
  const robot_ros2_msgs__msg__IntList * input,
  robot_ros2_msgs__msg__IntList * output)
{
  if (!input || !output) {
    return false;
  }
  // data
  if (!rosidl_runtime_c__int32__Sequence__copy(
      &(input->data), &(output->data)))
  {
    return false;
  }
  return true;
}

robot_ros2_msgs__msg__IntList *
robot_ros2_msgs__msg__IntList__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  robot_ros2_msgs__msg__IntList * msg = (robot_ros2_msgs__msg__IntList *)allocator.allocate(sizeof(robot_ros2_msgs__msg__IntList), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(robot_ros2_msgs__msg__IntList));
  bool success = robot_ros2_msgs__msg__IntList__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
robot_ros2_msgs__msg__IntList__destroy(robot_ros2_msgs__msg__IntList * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    robot_ros2_msgs__msg__IntList__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
robot_ros2_msgs__msg__IntList__Sequence__init(robot_ros2_msgs__msg__IntList__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  robot_ros2_msgs__msg__IntList * data = NULL;

  if (size) {
    data = (robot_ros2_msgs__msg__IntList *)allocator.zero_allocate(size, sizeof(robot_ros2_msgs__msg__IntList), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = robot_ros2_msgs__msg__IntList__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        robot_ros2_msgs__msg__IntList__fini(&data[i - 1]);
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
robot_ros2_msgs__msg__IntList__Sequence__fini(robot_ros2_msgs__msg__IntList__Sequence * array)
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
      robot_ros2_msgs__msg__IntList__fini(&array->data[i]);
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

robot_ros2_msgs__msg__IntList__Sequence *
robot_ros2_msgs__msg__IntList__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  robot_ros2_msgs__msg__IntList__Sequence * array = (robot_ros2_msgs__msg__IntList__Sequence *)allocator.allocate(sizeof(robot_ros2_msgs__msg__IntList__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = robot_ros2_msgs__msg__IntList__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
robot_ros2_msgs__msg__IntList__Sequence__destroy(robot_ros2_msgs__msg__IntList__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    robot_ros2_msgs__msg__IntList__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
robot_ros2_msgs__msg__IntList__Sequence__are_equal(const robot_ros2_msgs__msg__IntList__Sequence * lhs, const robot_ros2_msgs__msg__IntList__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!robot_ros2_msgs__msg__IntList__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
robot_ros2_msgs__msg__IntList__Sequence__copy(
  const robot_ros2_msgs__msg__IntList__Sequence * input,
  robot_ros2_msgs__msg__IntList__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(robot_ros2_msgs__msg__IntList);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    robot_ros2_msgs__msg__IntList * data =
      (robot_ros2_msgs__msg__IntList *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!robot_ros2_msgs__msg__IntList__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          robot_ros2_msgs__msg__IntList__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!robot_ros2_msgs__msg__IntList__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
