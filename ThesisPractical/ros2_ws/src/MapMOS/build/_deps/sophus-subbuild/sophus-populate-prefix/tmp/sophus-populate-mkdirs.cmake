# Distributed under the OSI-approved BSD 3-Clause License.  See accompanying
# file Copyright.txt or https://cmake.org/licensing for details.

cmake_minimum_required(VERSION 3.5)

file(MAKE_DIRECTORY
  "/home/mihkel/School/ThesisPractical/ros2_ws/src/MapMOS/build/_deps/sophus-src"
  "/home/mihkel/School/ThesisPractical/ros2_ws/src/MapMOS/build/_deps/sophus-build"
  "/home/mihkel/School/ThesisPractical/ros2_ws/src/MapMOS/build/_deps/sophus-subbuild/sophus-populate-prefix"
  "/home/mihkel/School/ThesisPractical/ros2_ws/src/MapMOS/build/_deps/sophus-subbuild/sophus-populate-prefix/tmp"
  "/home/mihkel/School/ThesisPractical/ros2_ws/src/MapMOS/build/_deps/sophus-subbuild/sophus-populate-prefix/src/sophus-populate-stamp"
  "/home/mihkel/School/ThesisPractical/ros2_ws/src/MapMOS/build/_deps/sophus-subbuild/sophus-populate-prefix/src"
  "/home/mihkel/School/ThesisPractical/ros2_ws/src/MapMOS/build/_deps/sophus-subbuild/sophus-populate-prefix/src/sophus-populate-stamp"
)

set(configSubDirs )
foreach(subDir IN LISTS configSubDirs)
    file(MAKE_DIRECTORY "/home/mihkel/School/ThesisPractical/ros2_ws/src/MapMOS/build/_deps/sophus-subbuild/sophus-populate-prefix/src/sophus-populate-stamp/${subDir}")
endforeach()
if(cfgdir)
  file(MAKE_DIRECTORY "/home/mihkel/School/ThesisPractical/ros2_ws/src/MapMOS/build/_deps/sophus-subbuild/sophus-populate-prefix/src/sophus-populate-stamp${cfgdir}") # cfgdir has leading slash
endif()
