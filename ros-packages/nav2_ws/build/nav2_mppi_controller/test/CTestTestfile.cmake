# CMake generated Testfile for 
# Source directory: /home/mihkel/School/ros-packages/nav2_ws/src/navigation2/nav2_mppi_controller/test
# Build directory: /home/mihkel/School/ros-packages/nav2_ws/build/nav2_mppi_controller/test
# 
# This file includes the relevant testing commands required for 
# testing this directory and lists subdirectories to be tested as well.
add_test(optimizer_smoke_test "/usr/bin/python3.10" "-u" "/opt/ros/humble/share/ament_cmake_test/cmake/run_test.py" "/home/mihkel/School/ros-packages/nav2_ws/build/nav2_mppi_controller/test_results/nav2_mppi_controller/optimizer_smoke_test.gtest.xml" "--package-name" "nav2_mppi_controller" "--output-file" "/home/mihkel/School/ros-packages/nav2_ws/build/nav2_mppi_controller/ament_cmake_gtest/optimizer_smoke_test.txt" "--command" "/home/mihkel/School/ros-packages/nav2_ws/build/nav2_mppi_controller/test/optimizer_smoke_test" "--gtest_output=xml:/home/mihkel/School/ros-packages/nav2_ws/build/nav2_mppi_controller/test_results/nav2_mppi_controller/optimizer_smoke_test.gtest.xml")
set_tests_properties(optimizer_smoke_test PROPERTIES  LABELS "gtest" REQUIRED_FILES "/home/mihkel/School/ros-packages/nav2_ws/build/nav2_mppi_controller/test/optimizer_smoke_test" TIMEOUT "60" WORKING_DIRECTORY "/home/mihkel/School/ros-packages/nav2_ws/build/nav2_mppi_controller/test" _BACKTRACE_TRIPLES "/opt/ros/humble/share/ament_cmake_test/cmake/ament_add_test.cmake;125;add_test;/opt/ros/humble/share/ament_cmake_gtest/cmake/ament_add_gtest_test.cmake;86;ament_add_test;/opt/ros/humble/share/ament_cmake_gtest/cmake/ament_add_gtest.cmake;93;ament_add_gtest_test;/home/mihkel/School/ros-packages/nav2_ws/src/navigation2/nav2_mppi_controller/test/CMakeLists.txt;16;ament_add_gtest;/home/mihkel/School/ros-packages/nav2_ws/src/navigation2/nav2_mppi_controller/test/CMakeLists.txt;0;")
add_test(controller_state_transition_test "/usr/bin/python3.10" "-u" "/opt/ros/humble/share/ament_cmake_test/cmake/run_test.py" "/home/mihkel/School/ros-packages/nav2_ws/build/nav2_mppi_controller/test_results/nav2_mppi_controller/controller_state_transition_test.gtest.xml" "--package-name" "nav2_mppi_controller" "--output-file" "/home/mihkel/School/ros-packages/nav2_ws/build/nav2_mppi_controller/ament_cmake_gtest/controller_state_transition_test.txt" "--command" "/home/mihkel/School/ros-packages/nav2_ws/build/nav2_mppi_controller/test/controller_state_transition_test" "--gtest_output=xml:/home/mihkel/School/ros-packages/nav2_ws/build/nav2_mppi_controller/test_results/nav2_mppi_controller/controller_state_transition_test.gtest.xml")
set_tests_properties(controller_state_transition_test PROPERTIES  LABELS "gtest" REQUIRED_FILES "/home/mihkel/School/ros-packages/nav2_ws/build/nav2_mppi_controller/test/controller_state_transition_test" TIMEOUT "60" WORKING_DIRECTORY "/home/mihkel/School/ros-packages/nav2_ws/build/nav2_mppi_controller/test" _BACKTRACE_TRIPLES "/opt/ros/humble/share/ament_cmake_test/cmake/ament_add_test.cmake;125;add_test;/opt/ros/humble/share/ament_cmake_gtest/cmake/ament_add_gtest_test.cmake;86;ament_add_test;/opt/ros/humble/share/ament_cmake_gtest/cmake/ament_add_gtest.cmake;93;ament_add_gtest_test;/home/mihkel/School/ros-packages/nav2_ws/src/navigation2/nav2_mppi_controller/test/CMakeLists.txt;16;ament_add_gtest;/home/mihkel/School/ros-packages/nav2_ws/src/navigation2/nav2_mppi_controller/test/CMakeLists.txt;0;")
add_test(models_test "/usr/bin/python3.10" "-u" "/opt/ros/humble/share/ament_cmake_test/cmake/run_test.py" "/home/mihkel/School/ros-packages/nav2_ws/build/nav2_mppi_controller/test_results/nav2_mppi_controller/models_test.gtest.xml" "--package-name" "nav2_mppi_controller" "--output-file" "/home/mihkel/School/ros-packages/nav2_ws/build/nav2_mppi_controller/ament_cmake_gtest/models_test.txt" "--command" "/home/mihkel/School/ros-packages/nav2_ws/build/nav2_mppi_controller/test/models_test" "--gtest_output=xml:/home/mihkel/School/ros-packages/nav2_ws/build/nav2_mppi_controller/test_results/nav2_mppi_controller/models_test.gtest.xml")
set_tests_properties(models_test PROPERTIES  LABELS "gtest" REQUIRED_FILES "/home/mihkel/School/ros-packages/nav2_ws/build/nav2_mppi_controller/test/models_test" TIMEOUT "60" WORKING_DIRECTORY "/home/mihkel/School/ros-packages/nav2_ws/build/nav2_mppi_controller/test" _BACKTRACE_TRIPLES "/opt/ros/humble/share/ament_cmake_test/cmake/ament_add_test.cmake;125;add_test;/opt/ros/humble/share/ament_cmake_gtest/cmake/ament_add_gtest_test.cmake;86;ament_add_test;/opt/ros/humble/share/ament_cmake_gtest/cmake/ament_add_gtest.cmake;93;ament_add_gtest_test;/home/mihkel/School/ros-packages/nav2_ws/src/navigation2/nav2_mppi_controller/test/CMakeLists.txt;16;ament_add_gtest;/home/mihkel/School/ros-packages/nav2_ws/src/navigation2/nav2_mppi_controller/test/CMakeLists.txt;0;")
add_test(noise_generator_test "/usr/bin/python3.10" "-u" "/opt/ros/humble/share/ament_cmake_test/cmake/run_test.py" "/home/mihkel/School/ros-packages/nav2_ws/build/nav2_mppi_controller/test_results/nav2_mppi_controller/noise_generator_test.gtest.xml" "--package-name" "nav2_mppi_controller" "--output-file" "/home/mihkel/School/ros-packages/nav2_ws/build/nav2_mppi_controller/ament_cmake_gtest/noise_generator_test.txt" "--command" "/home/mihkel/School/ros-packages/nav2_ws/build/nav2_mppi_controller/test/noise_generator_test" "--gtest_output=xml:/home/mihkel/School/ros-packages/nav2_ws/build/nav2_mppi_controller/test_results/nav2_mppi_controller/noise_generator_test.gtest.xml")
set_tests_properties(noise_generator_test PROPERTIES  LABELS "gtest" REQUIRED_FILES "/home/mihkel/School/ros-packages/nav2_ws/build/nav2_mppi_controller/test/noise_generator_test" TIMEOUT "60" WORKING_DIRECTORY "/home/mihkel/School/ros-packages/nav2_ws/build/nav2_mppi_controller/test" _BACKTRACE_TRIPLES "/opt/ros/humble/share/ament_cmake_test/cmake/ament_add_test.cmake;125;add_test;/opt/ros/humble/share/ament_cmake_gtest/cmake/ament_add_gtest_test.cmake;86;ament_add_test;/opt/ros/humble/share/ament_cmake_gtest/cmake/ament_add_gtest.cmake;93;ament_add_gtest_test;/home/mihkel/School/ros-packages/nav2_ws/src/navigation2/nav2_mppi_controller/test/CMakeLists.txt;16;ament_add_gtest;/home/mihkel/School/ros-packages/nav2_ws/src/navigation2/nav2_mppi_controller/test/CMakeLists.txt;0;")
add_test(parameter_handler_test "/usr/bin/python3.10" "-u" "/opt/ros/humble/share/ament_cmake_test/cmake/run_test.py" "/home/mihkel/School/ros-packages/nav2_ws/build/nav2_mppi_controller/test_results/nav2_mppi_controller/parameter_handler_test.gtest.xml" "--package-name" "nav2_mppi_controller" "--output-file" "/home/mihkel/School/ros-packages/nav2_ws/build/nav2_mppi_controller/ament_cmake_gtest/parameter_handler_test.txt" "--command" "/home/mihkel/School/ros-packages/nav2_ws/build/nav2_mppi_controller/test/parameter_handler_test" "--gtest_output=xml:/home/mihkel/School/ros-packages/nav2_ws/build/nav2_mppi_controller/test_results/nav2_mppi_controller/parameter_handler_test.gtest.xml")
set_tests_properties(parameter_handler_test PROPERTIES  LABELS "gtest" REQUIRED_FILES "/home/mihkel/School/ros-packages/nav2_ws/build/nav2_mppi_controller/test/parameter_handler_test" TIMEOUT "60" WORKING_DIRECTORY "/home/mihkel/School/ros-packages/nav2_ws/build/nav2_mppi_controller/test" _BACKTRACE_TRIPLES "/opt/ros/humble/share/ament_cmake_test/cmake/ament_add_test.cmake;125;add_test;/opt/ros/humble/share/ament_cmake_gtest/cmake/ament_add_gtest_test.cmake;86;ament_add_test;/opt/ros/humble/share/ament_cmake_gtest/cmake/ament_add_gtest.cmake;93;ament_add_gtest_test;/home/mihkel/School/ros-packages/nav2_ws/src/navigation2/nav2_mppi_controller/test/CMakeLists.txt;16;ament_add_gtest;/home/mihkel/School/ros-packages/nav2_ws/src/navigation2/nav2_mppi_controller/test/CMakeLists.txt;0;")
add_test(motion_model_tests "/usr/bin/python3.10" "-u" "/opt/ros/humble/share/ament_cmake_test/cmake/run_test.py" "/home/mihkel/School/ros-packages/nav2_ws/build/nav2_mppi_controller/test_results/nav2_mppi_controller/motion_model_tests.gtest.xml" "--package-name" "nav2_mppi_controller" "--output-file" "/home/mihkel/School/ros-packages/nav2_ws/build/nav2_mppi_controller/ament_cmake_gtest/motion_model_tests.txt" "--command" "/home/mihkel/School/ros-packages/nav2_ws/build/nav2_mppi_controller/test/motion_model_tests" "--gtest_output=xml:/home/mihkel/School/ros-packages/nav2_ws/build/nav2_mppi_controller/test_results/nav2_mppi_controller/motion_model_tests.gtest.xml")
set_tests_properties(motion_model_tests PROPERTIES  LABELS "gtest" REQUIRED_FILES "/home/mihkel/School/ros-packages/nav2_ws/build/nav2_mppi_controller/test/motion_model_tests" TIMEOUT "60" WORKING_DIRECTORY "/home/mihkel/School/ros-packages/nav2_ws/build/nav2_mppi_controller/test" _BACKTRACE_TRIPLES "/opt/ros/humble/share/ament_cmake_test/cmake/ament_add_test.cmake;125;add_test;/opt/ros/humble/share/ament_cmake_gtest/cmake/ament_add_gtest_test.cmake;86;ament_add_test;/opt/ros/humble/share/ament_cmake_gtest/cmake/ament_add_gtest.cmake;93;ament_add_gtest_test;/home/mihkel/School/ros-packages/nav2_ws/src/navigation2/nav2_mppi_controller/test/CMakeLists.txt;16;ament_add_gtest;/home/mihkel/School/ros-packages/nav2_ws/src/navigation2/nav2_mppi_controller/test/CMakeLists.txt;0;")
add_test(trajectory_visualizer_tests "/usr/bin/python3.10" "-u" "/opt/ros/humble/share/ament_cmake_test/cmake/run_test.py" "/home/mihkel/School/ros-packages/nav2_ws/build/nav2_mppi_controller/test_results/nav2_mppi_controller/trajectory_visualizer_tests.gtest.xml" "--package-name" "nav2_mppi_controller" "--output-file" "/home/mihkel/School/ros-packages/nav2_ws/build/nav2_mppi_controller/ament_cmake_gtest/trajectory_visualizer_tests.txt" "--command" "/home/mihkel/School/ros-packages/nav2_ws/build/nav2_mppi_controller/test/trajectory_visualizer_tests" "--gtest_output=xml:/home/mihkel/School/ros-packages/nav2_ws/build/nav2_mppi_controller/test_results/nav2_mppi_controller/trajectory_visualizer_tests.gtest.xml")
set_tests_properties(trajectory_visualizer_tests PROPERTIES  LABELS "gtest" REQUIRED_FILES "/home/mihkel/School/ros-packages/nav2_ws/build/nav2_mppi_controller/test/trajectory_visualizer_tests" TIMEOUT "60" WORKING_DIRECTORY "/home/mihkel/School/ros-packages/nav2_ws/build/nav2_mppi_controller/test" _BACKTRACE_TRIPLES "/opt/ros/humble/share/ament_cmake_test/cmake/ament_add_test.cmake;125;add_test;/opt/ros/humble/share/ament_cmake_gtest/cmake/ament_add_gtest_test.cmake;86;ament_add_test;/opt/ros/humble/share/ament_cmake_gtest/cmake/ament_add_gtest.cmake;93;ament_add_gtest_test;/home/mihkel/School/ros-packages/nav2_ws/src/navigation2/nav2_mppi_controller/test/CMakeLists.txt;16;ament_add_gtest;/home/mihkel/School/ros-packages/nav2_ws/src/navigation2/nav2_mppi_controller/test/CMakeLists.txt;0;")
add_test(utils_test "/usr/bin/python3.10" "-u" "/opt/ros/humble/share/ament_cmake_test/cmake/run_test.py" "/home/mihkel/School/ros-packages/nav2_ws/build/nav2_mppi_controller/test_results/nav2_mppi_controller/utils_test.gtest.xml" "--package-name" "nav2_mppi_controller" "--output-file" "/home/mihkel/School/ros-packages/nav2_ws/build/nav2_mppi_controller/ament_cmake_gtest/utils_test.txt" "--command" "/home/mihkel/School/ros-packages/nav2_ws/build/nav2_mppi_controller/test/utils_test" "--gtest_output=xml:/home/mihkel/School/ros-packages/nav2_ws/build/nav2_mppi_controller/test_results/nav2_mppi_controller/utils_test.gtest.xml")
set_tests_properties(utils_test PROPERTIES  LABELS "gtest" REQUIRED_FILES "/home/mihkel/School/ros-packages/nav2_ws/build/nav2_mppi_controller/test/utils_test" TIMEOUT "60" WORKING_DIRECTORY "/home/mihkel/School/ros-packages/nav2_ws/build/nav2_mppi_controller/test" _BACKTRACE_TRIPLES "/opt/ros/humble/share/ament_cmake_test/cmake/ament_add_test.cmake;125;add_test;/opt/ros/humble/share/ament_cmake_gtest/cmake/ament_add_gtest_test.cmake;86;ament_add_test;/opt/ros/humble/share/ament_cmake_gtest/cmake/ament_add_gtest.cmake;93;ament_add_gtest_test;/home/mihkel/School/ros-packages/nav2_ws/src/navigation2/nav2_mppi_controller/test/CMakeLists.txt;16;ament_add_gtest;/home/mihkel/School/ros-packages/nav2_ws/src/navigation2/nav2_mppi_controller/test/CMakeLists.txt;0;")
add_test(path_handler_test "/usr/bin/python3.10" "-u" "/opt/ros/humble/share/ament_cmake_test/cmake/run_test.py" "/home/mihkel/School/ros-packages/nav2_ws/build/nav2_mppi_controller/test_results/nav2_mppi_controller/path_handler_test.gtest.xml" "--package-name" "nav2_mppi_controller" "--output-file" "/home/mihkel/School/ros-packages/nav2_ws/build/nav2_mppi_controller/ament_cmake_gtest/path_handler_test.txt" "--command" "/home/mihkel/School/ros-packages/nav2_ws/build/nav2_mppi_controller/test/path_handler_test" "--gtest_output=xml:/home/mihkel/School/ros-packages/nav2_ws/build/nav2_mppi_controller/test_results/nav2_mppi_controller/path_handler_test.gtest.xml")
set_tests_properties(path_handler_test PROPERTIES  LABELS "gtest" REQUIRED_FILES "/home/mihkel/School/ros-packages/nav2_ws/build/nav2_mppi_controller/test/path_handler_test" TIMEOUT "60" WORKING_DIRECTORY "/home/mihkel/School/ros-packages/nav2_ws/build/nav2_mppi_controller/test" _BACKTRACE_TRIPLES "/opt/ros/humble/share/ament_cmake_test/cmake/ament_add_test.cmake;125;add_test;/opt/ros/humble/share/ament_cmake_gtest/cmake/ament_add_gtest_test.cmake;86;ament_add_test;/opt/ros/humble/share/ament_cmake_gtest/cmake/ament_add_gtest.cmake;93;ament_add_gtest_test;/home/mihkel/School/ros-packages/nav2_ws/src/navigation2/nav2_mppi_controller/test/CMakeLists.txt;16;ament_add_gtest;/home/mihkel/School/ros-packages/nav2_ws/src/navigation2/nav2_mppi_controller/test/CMakeLists.txt;0;")
add_test(critic_manager_test "/usr/bin/python3.10" "-u" "/opt/ros/humble/share/ament_cmake_test/cmake/run_test.py" "/home/mihkel/School/ros-packages/nav2_ws/build/nav2_mppi_controller/test_results/nav2_mppi_controller/critic_manager_test.gtest.xml" "--package-name" "nav2_mppi_controller" "--output-file" "/home/mihkel/School/ros-packages/nav2_ws/build/nav2_mppi_controller/ament_cmake_gtest/critic_manager_test.txt" "--command" "/home/mihkel/School/ros-packages/nav2_ws/build/nav2_mppi_controller/test/critic_manager_test" "--gtest_output=xml:/home/mihkel/School/ros-packages/nav2_ws/build/nav2_mppi_controller/test_results/nav2_mppi_controller/critic_manager_test.gtest.xml")
set_tests_properties(critic_manager_test PROPERTIES  LABELS "gtest" REQUIRED_FILES "/home/mihkel/School/ros-packages/nav2_ws/build/nav2_mppi_controller/test/critic_manager_test" TIMEOUT "60" WORKING_DIRECTORY "/home/mihkel/School/ros-packages/nav2_ws/build/nav2_mppi_controller/test" _BACKTRACE_TRIPLES "/opt/ros/humble/share/ament_cmake_test/cmake/ament_add_test.cmake;125;add_test;/opt/ros/humble/share/ament_cmake_gtest/cmake/ament_add_gtest_test.cmake;86;ament_add_test;/opt/ros/humble/share/ament_cmake_gtest/cmake/ament_add_gtest.cmake;93;ament_add_gtest_test;/home/mihkel/School/ros-packages/nav2_ws/src/navigation2/nav2_mppi_controller/test/CMakeLists.txt;16;ament_add_gtest;/home/mihkel/School/ros-packages/nav2_ws/src/navigation2/nav2_mppi_controller/test/CMakeLists.txt;0;")
add_test(optimizer_unit_tests "/usr/bin/python3.10" "-u" "/opt/ros/humble/share/ament_cmake_test/cmake/run_test.py" "/home/mihkel/School/ros-packages/nav2_ws/build/nav2_mppi_controller/test_results/nav2_mppi_controller/optimizer_unit_tests.gtest.xml" "--package-name" "nav2_mppi_controller" "--output-file" "/home/mihkel/School/ros-packages/nav2_ws/build/nav2_mppi_controller/ament_cmake_gtest/optimizer_unit_tests.txt" "--command" "/home/mihkel/School/ros-packages/nav2_ws/build/nav2_mppi_controller/test/optimizer_unit_tests" "--gtest_output=xml:/home/mihkel/School/ros-packages/nav2_ws/build/nav2_mppi_controller/test_results/nav2_mppi_controller/optimizer_unit_tests.gtest.xml")
set_tests_properties(optimizer_unit_tests PROPERTIES  LABELS "gtest" REQUIRED_FILES "/home/mihkel/School/ros-packages/nav2_ws/build/nav2_mppi_controller/test/optimizer_unit_tests" TIMEOUT "60" WORKING_DIRECTORY "/home/mihkel/School/ros-packages/nav2_ws/build/nav2_mppi_controller/test" _BACKTRACE_TRIPLES "/opt/ros/humble/share/ament_cmake_test/cmake/ament_add_test.cmake;125;add_test;/opt/ros/humble/share/ament_cmake_gtest/cmake/ament_add_gtest_test.cmake;86;ament_add_test;/opt/ros/humble/share/ament_cmake_gtest/cmake/ament_add_gtest.cmake;93;ament_add_gtest_test;/home/mihkel/School/ros-packages/nav2_ws/src/navigation2/nav2_mppi_controller/test/CMakeLists.txt;16;ament_add_gtest;/home/mihkel/School/ros-packages/nav2_ws/src/navigation2/nav2_mppi_controller/test/CMakeLists.txt;0;")
add_test(critics_tests "/usr/bin/python3.10" "-u" "/opt/ros/humble/share/ament_cmake_test/cmake/run_test.py" "/home/mihkel/School/ros-packages/nav2_ws/build/nav2_mppi_controller/test_results/nav2_mppi_controller/critics_tests.gtest.xml" "--package-name" "nav2_mppi_controller" "--output-file" "/home/mihkel/School/ros-packages/nav2_ws/build/nav2_mppi_controller/ament_cmake_gtest/critics_tests.txt" "--command" "/home/mihkel/School/ros-packages/nav2_ws/build/nav2_mppi_controller/test/critics_tests" "--gtest_output=xml:/home/mihkel/School/ros-packages/nav2_ws/build/nav2_mppi_controller/test_results/nav2_mppi_controller/critics_tests.gtest.xml")
set_tests_properties(critics_tests PROPERTIES  LABELS "gtest" REQUIRED_FILES "/home/mihkel/School/ros-packages/nav2_ws/build/nav2_mppi_controller/test/critics_tests" TIMEOUT "60" WORKING_DIRECTORY "/home/mihkel/School/ros-packages/nav2_ws/build/nav2_mppi_controller/test" _BACKTRACE_TRIPLES "/opt/ros/humble/share/ament_cmake_test/cmake/ament_add_test.cmake;125;add_test;/opt/ros/humble/share/ament_cmake_gtest/cmake/ament_add_gtest_test.cmake;86;ament_add_test;/opt/ros/humble/share/ament_cmake_gtest/cmake/ament_add_gtest.cmake;93;ament_add_gtest_test;/home/mihkel/School/ros-packages/nav2_ws/src/navigation2/nav2_mppi_controller/test/CMakeLists.txt;35;ament_add_gtest;/home/mihkel/School/ros-packages/nav2_ws/src/navigation2/nav2_mppi_controller/test/CMakeLists.txt;0;")
subdirs("../gtest")
