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
include common/fw/CMakeFiles/fw.dir/depend.make
# Include any dependencies generated by the compiler for this target.
include common/fw/CMakeFiles/fw.dir/compiler_depend.make

# Include the progress variables for this target.
include common/fw/CMakeFiles/fw.dir/progress.make

# Include the compile flags for this target's objects.
include common/fw/CMakeFiles/fw.dir/flags.make

common/fw/CMakeFiles/fw.dir/empty.c.o: common/fw/CMakeFiles/fw.dir/flags.make
common/fw/CMakeFiles/fw.dir/empty.c.o: ../common/fw/empty.c
common/fw/CMakeFiles/fw.dir/empty.c.o: common/fw/CMakeFiles/fw.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/mihkel/School/ThesisPractical/librealsense/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building C object common/fw/CMakeFiles/fw.dir/empty.c.o"
	cd /home/mihkel/School/ThesisPractical/librealsense/build/common/fw && /usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -MD -MT common/fw/CMakeFiles/fw.dir/empty.c.o -MF CMakeFiles/fw.dir/empty.c.o.d -o CMakeFiles/fw.dir/empty.c.o -c /home/mihkel/School/ThesisPractical/librealsense/common/fw/empty.c

common/fw/CMakeFiles/fw.dir/empty.c.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing C source to CMakeFiles/fw.dir/empty.c.i"
	cd /home/mihkel/School/ThesisPractical/librealsense/build/common/fw && /usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -E /home/mihkel/School/ThesisPractical/librealsense/common/fw/empty.c > CMakeFiles/fw.dir/empty.c.i

common/fw/CMakeFiles/fw.dir/empty.c.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling C source to assembly CMakeFiles/fw.dir/empty.c.s"
	cd /home/mihkel/School/ThesisPractical/librealsense/build/common/fw && /usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -S /home/mihkel/School/ThesisPractical/librealsense/common/fw/empty.c -o CMakeFiles/fw.dir/empty.c.s

common/fw/CMakeFiles/fw.dir/D4XX_FW_Image.c.o: common/fw/CMakeFiles/fw.dir/flags.make
common/fw/CMakeFiles/fw.dir/D4XX_FW_Image.c.o: common/fw/D4XX_FW_Image.c
common/fw/CMakeFiles/fw.dir/D4XX_FW_Image.c.o: common/fw/D4XX_FW_Image-5.15.1.0.bin
common/fw/CMakeFiles/fw.dir/D4XX_FW_Image.c.o: common/fw/CMakeFiles/fw.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/mihkel/School/ThesisPractical/librealsense/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Building C object common/fw/CMakeFiles/fw.dir/D4XX_FW_Image.c.o"
	cd /home/mihkel/School/ThesisPractical/librealsense/build/common/fw && /usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -MD -MT common/fw/CMakeFiles/fw.dir/D4XX_FW_Image.c.o -MF CMakeFiles/fw.dir/D4XX_FW_Image.c.o.d -o CMakeFiles/fw.dir/D4XX_FW_Image.c.o -c /home/mihkel/School/ThesisPractical/librealsense/build/common/fw/D4XX_FW_Image.c

common/fw/CMakeFiles/fw.dir/D4XX_FW_Image.c.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing C source to CMakeFiles/fw.dir/D4XX_FW_Image.c.i"
	cd /home/mihkel/School/ThesisPractical/librealsense/build/common/fw && /usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -E /home/mihkel/School/ThesisPractical/librealsense/build/common/fw/D4XX_FW_Image.c > CMakeFiles/fw.dir/D4XX_FW_Image.c.i

common/fw/CMakeFiles/fw.dir/D4XX_FW_Image.c.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling C source to assembly CMakeFiles/fw.dir/D4XX_FW_Image.c.s"
	cd /home/mihkel/School/ThesisPractical/librealsense/build/common/fw && /usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -S /home/mihkel/School/ThesisPractical/librealsense/build/common/fw/D4XX_FW_Image.c -o CMakeFiles/fw.dir/D4XX_FW_Image.c.s

common/fw/CMakeFiles/fw.dir/SR3XX_FW_Image.c.o: common/fw/CMakeFiles/fw.dir/flags.make
common/fw/CMakeFiles/fw.dir/SR3XX_FW_Image.c.o: common/fw/SR3XX_FW_Image.c
common/fw/CMakeFiles/fw.dir/SR3XX_FW_Image.c.o: common/fw/SR3XX_FW_Image-3.26.1.0.bin
common/fw/CMakeFiles/fw.dir/SR3XX_FW_Image.c.o: common/fw/CMakeFiles/fw.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/mihkel/School/ThesisPractical/librealsense/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_3) "Building C object common/fw/CMakeFiles/fw.dir/SR3XX_FW_Image.c.o"
	cd /home/mihkel/School/ThesisPractical/librealsense/build/common/fw && /usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -MD -MT common/fw/CMakeFiles/fw.dir/SR3XX_FW_Image.c.o -MF CMakeFiles/fw.dir/SR3XX_FW_Image.c.o.d -o CMakeFiles/fw.dir/SR3XX_FW_Image.c.o -c /home/mihkel/School/ThesisPractical/librealsense/build/common/fw/SR3XX_FW_Image.c

common/fw/CMakeFiles/fw.dir/SR3XX_FW_Image.c.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing C source to CMakeFiles/fw.dir/SR3XX_FW_Image.c.i"
	cd /home/mihkel/School/ThesisPractical/librealsense/build/common/fw && /usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -E /home/mihkel/School/ThesisPractical/librealsense/build/common/fw/SR3XX_FW_Image.c > CMakeFiles/fw.dir/SR3XX_FW_Image.c.i

common/fw/CMakeFiles/fw.dir/SR3XX_FW_Image.c.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling C source to assembly CMakeFiles/fw.dir/SR3XX_FW_Image.c.s"
	cd /home/mihkel/School/ThesisPractical/librealsense/build/common/fw && /usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -S /home/mihkel/School/ThesisPractical/librealsense/build/common/fw/SR3XX_FW_Image.c -o CMakeFiles/fw.dir/SR3XX_FW_Image.c.s

common/fw/CMakeFiles/fw.dir/L51X_FW_Image.c.o: common/fw/CMakeFiles/fw.dir/flags.make
common/fw/CMakeFiles/fw.dir/L51X_FW_Image.c.o: common/fw/L51X_FW_Image.c
common/fw/CMakeFiles/fw.dir/L51X_FW_Image.c.o: common/fw/L51X_FW_Image-1.5.8.1.bin
common/fw/CMakeFiles/fw.dir/L51X_FW_Image.c.o: common/fw/CMakeFiles/fw.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/mihkel/School/ThesisPractical/librealsense/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_4) "Building C object common/fw/CMakeFiles/fw.dir/L51X_FW_Image.c.o"
	cd /home/mihkel/School/ThesisPractical/librealsense/build/common/fw && /usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -MD -MT common/fw/CMakeFiles/fw.dir/L51X_FW_Image.c.o -MF CMakeFiles/fw.dir/L51X_FW_Image.c.o.d -o CMakeFiles/fw.dir/L51X_FW_Image.c.o -c /home/mihkel/School/ThesisPractical/librealsense/build/common/fw/L51X_FW_Image.c

common/fw/CMakeFiles/fw.dir/L51X_FW_Image.c.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing C source to CMakeFiles/fw.dir/L51X_FW_Image.c.i"
	cd /home/mihkel/School/ThesisPractical/librealsense/build/common/fw && /usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -E /home/mihkel/School/ThesisPractical/librealsense/build/common/fw/L51X_FW_Image.c > CMakeFiles/fw.dir/L51X_FW_Image.c.i

common/fw/CMakeFiles/fw.dir/L51X_FW_Image.c.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling C source to assembly CMakeFiles/fw.dir/L51X_FW_Image.c.s"
	cd /home/mihkel/School/ThesisPractical/librealsense/build/common/fw && /usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -S /home/mihkel/School/ThesisPractical/librealsense/build/common/fw/L51X_FW_Image.c -o CMakeFiles/fw.dir/L51X_FW_Image.c.s

# Object files for target fw
fw_OBJECTS = \
"CMakeFiles/fw.dir/empty.c.o" \
"CMakeFiles/fw.dir/D4XX_FW_Image.c.o" \
"CMakeFiles/fw.dir/SR3XX_FW_Image.c.o" \
"CMakeFiles/fw.dir/L51X_FW_Image.c.o"

# External object files for target fw
fw_EXTERNAL_OBJECTS =

common/fw/libfw.a: common/fw/CMakeFiles/fw.dir/empty.c.o
common/fw/libfw.a: common/fw/CMakeFiles/fw.dir/D4XX_FW_Image.c.o
common/fw/libfw.a: common/fw/CMakeFiles/fw.dir/SR3XX_FW_Image.c.o
common/fw/libfw.a: common/fw/CMakeFiles/fw.dir/L51X_FW_Image.c.o
common/fw/libfw.a: common/fw/CMakeFiles/fw.dir/build.make
common/fw/libfw.a: common/fw/CMakeFiles/fw.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/home/mihkel/School/ThesisPractical/librealsense/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_5) "Linking C static library libfw.a"
	cd /home/mihkel/School/ThesisPractical/librealsense/build/common/fw && $(CMAKE_COMMAND) -P CMakeFiles/fw.dir/cmake_clean_target.cmake
	cd /home/mihkel/School/ThesisPractical/librealsense/build/common/fw && $(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/fw.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
common/fw/CMakeFiles/fw.dir/build: common/fw/libfw.a
.PHONY : common/fw/CMakeFiles/fw.dir/build

common/fw/CMakeFiles/fw.dir/clean:
	cd /home/mihkel/School/ThesisPractical/librealsense/build/common/fw && $(CMAKE_COMMAND) -P CMakeFiles/fw.dir/cmake_clean.cmake
.PHONY : common/fw/CMakeFiles/fw.dir/clean

common/fw/CMakeFiles/fw.dir/depend:
	cd /home/mihkel/School/ThesisPractical/librealsense/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/mihkel/School/ThesisPractical/librealsense /home/mihkel/School/ThesisPractical/librealsense/common/fw /home/mihkel/School/ThesisPractical/librealsense/build /home/mihkel/School/ThesisPractical/librealsense/build/common/fw /home/mihkel/School/ThesisPractical/librealsense/build/common/fw/CMakeFiles/fw.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : common/fw/CMakeFiles/fw.dir/depend

