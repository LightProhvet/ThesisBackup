# Install script for directory: /home/mihkel/School/ThesisPractical/rtabmap_ws/src/rtabmap

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "/home/mihkel/School/ThesisPractical/rtabmap_ws/install/rtabmap")
endif()
string(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
if(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  if(BUILD_TYPE)
    string(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  else()
    set(CMAKE_INSTALL_CONFIG_NAME "Release")
  endif()
  message(STATUS "Install configuration: \"${CMAKE_INSTALL_CONFIG_NAME}\"")
endif()

# Set the component getting installed.
if(NOT CMAKE_INSTALL_COMPONENT)
  if(COMPONENT)
    message(STATUS "Install component: \"${COMPONENT}\"")
    set(CMAKE_INSTALL_COMPONENT "${COMPONENT}")
  else()
    set(CMAKE_INSTALL_COMPONENT)
  endif()
endif()

# Install shared libraries without execute permission?
if(NOT DEFINED CMAKE_INSTALL_SO_NO_EXE)
  set(CMAKE_INSTALL_SO_NO_EXE "1")
endif()

# Is this installation the result of a crosscompile?
if(NOT DEFINED CMAKE_CROSSCOMPILING)
  set(CMAKE_CROSSCOMPILING "FALSE")
endif()

# Set default install directory permissions.
if(NOT DEFINED CMAKE_OBJDUMP)
  set(CMAKE_OBJDUMP "/usr/bin/objdump")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "devel" OR NOT CMAKE_INSTALL_COMPONENT)
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/rtabmap-0.21/RTABMapTargets.cmake")
    file(DIFFERENT _cmake_export_file_changed FILES
         "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/rtabmap-0.21/RTABMapTargets.cmake"
         "/home/mihkel/School/ThesisPractical/rtabmap_ws/build/rtabmap/CMakeFiles/Export/403f3fe847f0f7c53039da200a1c340a/RTABMapTargets.cmake")
    if(_cmake_export_file_changed)
      file(GLOB _cmake_old_config_files "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/rtabmap-0.21/RTABMapTargets-*.cmake")
      if(_cmake_old_config_files)
        string(REPLACE ";" ", " _cmake_old_config_files_text "${_cmake_old_config_files}")
        message(STATUS "Old export file \"$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/rtabmap-0.21/RTABMapTargets.cmake\" will be replaced.  Removing files [${_cmake_old_config_files_text}].")
        unset(_cmake_old_config_files_text)
        file(REMOVE ${_cmake_old_config_files})
      endif()
      unset(_cmake_old_config_files)
    endif()
    unset(_cmake_export_file_changed)
  endif()
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/rtabmap-0.21" TYPE FILE FILES "/home/mihkel/School/ThesisPractical/rtabmap_ws/build/rtabmap/CMakeFiles/Export/403f3fe847f0f7c53039da200a1c340a/RTABMapTargets.cmake")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "devel" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/rtabmap-0.21" TYPE FILE FILES
    "/home/mihkel/School/ThesisPractical/rtabmap_ws/build/rtabmap/CMakeFiles/RTABMapConfig.cmake"
    "/home/mihkel/School/ThesisPractical/rtabmap_ws/build/rtabmap/RTABMapConfigVersion.cmake"
    )
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "devel" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/rtabmap" TYPE FILE FILES "/home/mihkel/School/ThesisPractical/rtabmap_ws/src/rtabmap/package.xml")
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for each subdirectory.
  include("/home/mihkel/School/ThesisPractical/rtabmap_ws/build/rtabmap/utilite/cmake_install.cmake")
  include("/home/mihkel/School/ThesisPractical/rtabmap_ws/build/rtabmap/corelib/cmake_install.cmake")
  include("/home/mihkel/School/ThesisPractical/rtabmap_ws/build/rtabmap/guilib/cmake_install.cmake")
  include("/home/mihkel/School/ThesisPractical/rtabmap_ws/build/rtabmap/app/cmake_install.cmake")
  include("/home/mihkel/School/ThesisPractical/rtabmap_ws/build/rtabmap/tools/cmake_install.cmake")
  include("/home/mihkel/School/ThesisPractical/rtabmap_ws/build/rtabmap/examples/cmake_install.cmake")

endif()

if(CMAKE_INSTALL_COMPONENT)
  set(CMAKE_INSTALL_MANIFEST "install_manifest_${CMAKE_INSTALL_COMPONENT}.txt")
else()
  set(CMAKE_INSTALL_MANIFEST "install_manifest.txt")
endif()

string(REPLACE ";" "\n" CMAKE_INSTALL_MANIFEST_CONTENT
       "${CMAKE_INSTALL_MANIFEST_FILES}")
file(WRITE "/home/mihkel/School/ThesisPractical/rtabmap_ws/build/rtabmap/${CMAKE_INSTALL_MANIFEST}"
     "${CMAKE_INSTALL_MANIFEST_CONTENT}")
