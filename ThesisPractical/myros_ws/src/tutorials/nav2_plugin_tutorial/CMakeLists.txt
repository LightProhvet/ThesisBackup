cmake_minimum_required(VERSION 3.8)
project(nav2_plugin_tutorial)

# env
if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# build
set (lib_name ${PROJECT_NAME}_core)  # although this is needed elsewhere too

add_library(${lib_name} SHARED
  src/tutorial_costmap_plugin.cpp
)
include_directories(include)

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(nav2_costmap_2d REQUIRED)
find_package(pluginlib REQUIRED)

# easier set of target dependencies
set(dep_pkgs
    rclcpp
    nav2_costmap_2d
    pluginlib)

# install
install(TARGETS ${lib_name}
        DESTINATION lib)
# Ament/ build work

# pluginlib_export_plugin_description_file() installs gradient_layer.xml
# file into "share" directory and sets ament indexes for it.
# This allows the plugin to be discovered as a plugin of required type.
pluginlib_export_plugin_description_file(nav2_costmap_2d tutorial_layer.xml)
ament_target_dependencies(${lib_name} ${dep_pkgs})

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  # the following line skips the linter which checks for copyrights
  # comment the line when a copyright and license is added to all source files
  set(ament_cmake_copyright_FOUND TRUE)
  # the following line skips cpplint (only works in a git repo)
  # comment the line when this package is in a git repo and when
  # a copyright and license is added to all source files
  set(ament_cmake_cpplint_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()

ament_package()
