# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.22

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:

#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:

# Disable VCS-based implicit rules.
% : %,v

# Disable VCS-based implicit rules.
% : RCS/%

# Disable VCS-based implicit rules.
% : RCS/%,v

# Disable VCS-based implicit rules.
% : SCCS/s.%

# Disable VCS-based implicit rules.
% : s.%

.SUFFIXES: .hpux_make_needs_suffix_list

# Command-line flag to silence nested $(MAKE).
$(VERBOSE)MAKESILENT = -s

#Suppress display of executed commands.
$(VERBOSE).SILENT:

# A target that is always out of date.
cmake_force:
.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /usr/bin/cmake

# The command to remove a file.
RM = /usr/bin/cmake -E rm -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /home/mihkel/School/ThesisPractical/librealsense

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /home/mihkel/School/ThesisPractical/librealsense/build

# Include any dependencies generated for this target.
include examples/software-device/CMakeFiles/rs-software-device.dir/depend.make
# Include any dependencies generated by the compiler for this target.
include examples/software-device/CMakeFiles/rs-software-device.dir/compiler_depend.make

# Include the progress variables for this target.
include examples/software-device/CMakeFiles/rs-software-device.dir/progress.make

# Include the compile flags for this target's objects.
include examples/software-device/CMakeFiles/rs-software-device.dir/flags.make

examples/software-device/CMakeFiles/rs-software-device.dir/rs-software-device.cpp.o: examples/software-device/CMakeFiles/rs-software-device.dir/flags.make
examples/software-device/CMakeFiles/rs-software-device.dir/rs-software-device.cpp.o: ../examples/software-device/rs-software-device.cpp
examples/software-device/CMakeFiles/rs-software-device.dir/rs-software-device.cpp.o: examples/software-device/CMakeFiles/rs-software-device.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/mihkel/School/ThesisPractical/librealsense/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object examples/software-device/CMakeFiles/rs-software-device.dir/rs-software-device.cpp.o"
	cd /home/mihkel/School/ThesisPractical/librealsense/build/examples/software-device && /usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT examples/software-device/CMakeFiles/rs-software-device.dir/rs-software-device.cpp.o -MF CMakeFiles/rs-software-device.dir/rs-software-device.cpp.o.d -o CMakeFiles/rs-software-device.dir/rs-software-device.cpp.o -c /home/mihkel/School/ThesisPractical/librealsense/examples/software-device/rs-software-device.cpp

examples/software-device/CMakeFiles/rs-software-device.dir/rs-software-device.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/rs-software-device.dir/rs-software-device.cpp.i"
	cd /home/mihkel/School/ThesisPractical/librealsense/build/examples/software-device && /usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /home/mihkel/School/ThesisPractical/librealsense/examples/software-device/rs-software-device.cpp > CMakeFiles/rs-software-device.dir/rs-software-device.cpp.i

examples/software-device/CMakeFiles/rs-software-device.dir/rs-software-device.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/rs-software-device.dir/rs-software-device.cpp.s"
	cd /home/mihkel/School/ThesisPractical/librealsense/build/examples/software-device && /usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /home/mihkel/School/ThesisPractical/librealsense/examples/software-device/rs-software-device.cpp -o CMakeFiles/rs-software-device.dir/rs-software-device.cpp.s

# Object files for target rs-software-device
rs__software__device_OBJECTS = \
"CMakeFiles/rs-software-device.dir/rs-software-device.cpp.o"

# External object files for target rs-software-device
rs__software__device_EXTERNAL_OBJECTS =

Release/rs-software-device: examples/software-device/CMakeFiles/rs-software-device.dir/rs-software-device.cpp.o
Release/rs-software-device: examples/software-device/CMakeFiles/rs-software-device.dir/build.make
Release/rs-software-device: Release/librealsense2.so.2.54.2
Release/rs-software-device: /usr/lib/x86_64-linux-gnu/libglfw.so.3.3
Release/rs-software-device: /usr/lib/x86_64-linux-gnu/libOpenGL.so
Release/rs-software-device: /usr/lib/x86_64-linux-gnu/libGLX.so
Release/rs-software-device: /usr/lib/x86_64-linux-gnu/libGLU.so
Release/rs-software-device: third-party/rsutils/librsutils.a
Release/rs-software-device: examples/software-device/CMakeFiles/rs-software-device.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/home/mihkel/School/ThesisPractical/librealsense/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking CXX executable ../../Release/rs-software-device"
	cd /home/mihkel/School/ThesisPractical/librealsense/build/examples/software-device && $(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/rs-software-device.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
examples/software-device/CMakeFiles/rs-software-device.dir/build: Release/rs-software-device
.PHONY : examples/software-device/CMakeFiles/rs-software-device.dir/build

examples/software-device/CMakeFiles/rs-software-device.dir/clean:
	cd /home/mihkel/School/ThesisPractical/librealsense/build/examples/software-device && $(CMAKE_COMMAND) -P CMakeFiles/rs-software-device.dir/cmake_clean.cmake
.PHONY : examples/software-device/CMakeFiles/rs-software-device.dir/clean

examples/software-device/CMakeFiles/rs-software-device.dir/depend:
	cd /home/mihkel/School/ThesisPractical/librealsense/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/mihkel/School/ThesisPractical/librealsense /home/mihkel/School/ThesisPractical/librealsense/examples/software-device /home/mihkel/School/ThesisPractical/librealsense/build /home/mihkel/School/ThesisPractical/librealsense/build/examples/software-device /home/mihkel/School/ThesisPractical/librealsense/build/examples/software-device/CMakeFiles/rs-software-device.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : examples/software-device/CMakeFiles/rs-software-device.dir/depend

