# Distributed under the OSI-approved BSD 3-Clause License.  See accompanying
# file Copyright.txt or https://cmake.org/licensing for details.

cmake_minimum_required(VERSION 3.5)

file(MAKE_DIRECTORY
  "/home/mihkel/School/ThesisPractical/ros2_ws/src/MapMOS/build/_deps/tessil-src"
  "/home/mihkel/School/ThesisPractical/ros2_ws/src/MapMOS/build/_deps/tessil-build"
  "/home/mihkel/School/ThesisPractical/ros2_ws/src/MapMOS/build/_deps/tessil-subbuild/tessil-populate-prefix"
  "/home/mihkel/School/ThesisPractical/ros2_ws/src/MapMOS/build/_deps/tessil-subbuild/tessil-populate-prefix/tmp"
  "/home/mihkel/School/ThesisPractical/ros2_ws/src/MapMOS/build/_deps/tessil-subbuild/tessil-populate-prefix/src/tessil-populate-stamp"
  "/home/mihkel/School/ThesisPractical/ros2_ws/src/MapMOS/build/_deps/tessil-subbuild/tessil-populate-prefix/src"
  "/home/mihkel/School/ThesisPractical/ros2_ws/src/MapMOS/build/_deps/tessil-subbuild/tessil-populate-prefix/src/tessil-populate-stamp"
)

set(configSubDirs )
foreach(subDir IN LISTS configSubDirs)
    file(MAKE_DIRECTORY "/home/mihkel/School/ThesisPractical/ros2_ws/src/MapMOS/build/_deps/tessil-subbuild/tessil-populate-prefix/src/tessil-populate-stamp/${subDir}")
endforeach()
if(cfgdir)
  file(MAKE_DIRECTORY "/home/mihkel/School/ThesisPractical/ros2_ws/src/MapMOS/build/_deps/tessil-subbuild/tessil-populate-prefix/src/tessil-populate-stamp${cfgdir}") # cfgdir has leading slash
endif()
