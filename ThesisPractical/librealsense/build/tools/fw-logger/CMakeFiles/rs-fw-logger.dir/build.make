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
include tools/fw-logger/CMakeFiles/rs-fw-logger.dir/depend.make
# Include any dependencies generated by the compiler for this target.
include tools/fw-logger/CMakeFiles/rs-fw-logger.dir/compiler_depend.make

# Include the progress variables for this target.
include tools/fw-logger/CMakeFiles/rs-fw-logger.dir/progress.make

# Include the compile flags for this target's objects.
include tools/fw-logger/CMakeFiles/rs-fw-logger.dir/flags.make

tools/fw-logger/CMakeFiles/rs-fw-logger.dir/rs-fw-logger.cpp.o: tools/fw-logger/CMakeFiles/rs-fw-logger.dir/flags.make
tools/fw-logger/CMakeFiles/rs-fw-logger.dir/rs-fw-logger.cpp.o: ../tools/fw-logger/rs-fw-logger.cpp
tools/fw-logger/CMakeFiles/rs-fw-logger.dir/rs-fw-logger.cpp.o: tools/fw-logger/CMakeFiles/rs-fw-logger.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/mihkel/School/ThesisPractical/librealsense/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object tools/fw-logger/CMakeFiles/rs-fw-logger.dir/rs-fw-logger.cpp.o"
	cd /home/mihkel/School/ThesisPractical/librealsense/build/tools/fw-logger && /usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT tools/fw-logger/CMakeFiles/rs-fw-logger.dir/rs-fw-logger.cpp.o -MF CMakeFiles/rs-fw-logger.dir/rs-fw-logger.cpp.o.d -o CMakeFiles/rs-fw-logger.dir/rs-fw-logger.cpp.o -c /home/mihkel/School/ThesisPractical/librealsense/tools/fw-logger/rs-fw-logger.cpp

tools/fw-logger/CMakeFiles/rs-fw-logger.dir/rs-fw-logger.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/rs-fw-logger.dir/rs-fw-logger.cpp.i"
	cd /home/mihkel/School/ThesisPractical/librealsense/build/tools/fw-logger && /usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /home/mihkel/School/ThesisPractical/librealsense/tools/fw-logger/rs-fw-logger.cpp > CMakeFiles/rs-fw-logger.dir/rs-fw-logger.cpp.i

tools/fw-logger/CMakeFiles/rs-fw-logger.dir/rs-fw-logger.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/rs-fw-logger.dir/rs-fw-logger.cpp.s"
	cd /home/mihkel/School/ThesisPractical/librealsense/build/tools/fw-logger && /usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /home/mihkel/School/ThesisPractical/librealsense/tools/fw-logger/rs-fw-logger.cpp -o CMakeFiles/rs-fw-logger.dir/rs-fw-logger.cpp.s

# Object files for target rs-fw-logger
rs__fw__logger_OBJECTS = \
"CMakeFiles/rs-fw-logger.dir/rs-fw-logger.cpp.o"

# External object files for target rs-fw-logger
rs__fw__logger_EXTERNAL_OBJECTS =

Release/rs-fw-logger: tools/fw-logger/CMakeFiles/rs-fw-logger.dir/rs-fw-logger.cpp.o
Release/rs-fw-logger: tools/fw-logger/CMakeFiles/rs-fw-logger.dir/build.make
Release/rs-fw-logger: Release/librealsense2.so.2.54.2
Release/rs-fw-logger: third-party/rsutils/librsutils.a
Release/rs-fw-logger: tools/fw-logger/CMakeFiles/rs-fw-logger.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/home/mihkel/School/ThesisPractical/librealsense/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking CXX executable ../../Release/rs-fw-logger"
	cd /home/mihkel/School/ThesisPractical/librealsense/build/tools/fw-logger && $(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/rs-fw-logger.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
tools/fw-logger/CMakeFiles/rs-fw-logger.dir/build: Release/rs-fw-logger
.PHONY : tools/fw-logger/CMakeFiles/rs-fw-logger.dir/build

tools/fw-logger/CMakeFiles/rs-fw-logger.dir/clean:
	cd /home/mihkel/School/ThesisPractical/librealsense/build/tools/fw-logger && $(CMAKE_COMMAND) -P CMakeFiles/rs-fw-logger.dir/cmake_clean.cmake
.PHONY : tools/fw-logger/CMakeFiles/rs-fw-logger.dir/clean

tools/fw-logger/CMakeFiles/rs-fw-logger.dir/depend:
	cd /home/mihkel/School/ThesisPractical/librealsense/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/mihkel/School/ThesisPractical/librealsense /home/mihkel/School/ThesisPractical/librealsense/tools/fw-logger /home/mihkel/School/ThesisPractical/librealsense/build /home/mihkel/School/ThesisPractical/librealsense/build/tools/fw-logger /home/mihkel/School/ThesisPractical/librealsense/build/tools/fw-logger/CMakeFiles/rs-fw-logger.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : tools/fw-logger/CMakeFiles/rs-fw-logger.dir/depend

