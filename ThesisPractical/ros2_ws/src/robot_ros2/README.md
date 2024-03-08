# RobotNet hospital carrier

## Requirements

ROS2 Humble (https://docs.ros.org/en/humble/Installation/Ubuntu-Install-Debians.html)   
Ubuntu 22.04   

## Install required packages for nodes

```bash
sudo apt-get install ros-humble-tf-transformations
sudo apt-get install ros-humble-depthimage-to-laserscan
sudo pip3 install transforms3d
pip3 install defusedxml
pip install paho-mqtt
pip install fibre
pip install odrive
pip install pyserial
pip install approxeng.input==2.6.2
pip install pyzbar
```

If you see `ModuleNotFoundError: No module named 'em'` then install `sudo apt-get install python3-empy`

## Installation of hospital carrier robot project

Make sure your version of setuptools is 58.2.0, otherwise you will get an error when trying to build.

```bash
pip3 install setuptools==58.2.0
```

Add the package and the messages package to your ros workspace and colcon build:

```bash
cd ~/ros2_ws/src && git clone https://gitlab.com/hospitalrobot/robot_ros2.git && git clone https://gitlab.com/hospitalrobot/robot-ros2-messages.git
cd ~/ros2_ws/ && colcon build
```
Make sure to source your workspace by using
```bash
source install/setup.bash
```
to use ros2 launch functionalities.

Also add the depthimage_to_laserscan package and rtabmap packages to your workspace (rtabmap installation explained below).
```bash
git clone https://github.com/ros-perception/depthimage_to_laserscan.git 
cd depthimage_to_laserscan/ && git checkout ros2
```

## Installing RealSense on Ubuntu

Install realsense for ros by following the steps here https://github.com/IntelRealSense/realsense-ros . Option 1 for both steps works fine. If one option fails, you can try other options.

## RealSense firmware

Please make sure RealSense cameras are running the latest firmware (firmware checking and update tool comes with *librealsense* installed in a previous section)

Latest [firmware](https://dev.intelrealsense.com/docs/firmware-releases)
```
# list devices
rs-fw-update -l
# update device with serial number XXX (outputted by previous command)
rs-fw-update -s XXX -f /path/to/Signed_Image_UVC_ZZZZZZ.bin
```

## Launch code on robot
**Launch on the actual robot**

Needs Odrives to be connected.

```bash
ros2 launch hospital_carrier hospital_robot.launch
```

## SLAM with Rtabmap

### Installation and setup

Install rtabmap. I recommend building both from source, otherwise it might not install RealSense support. Switch to ros2 branch in rtabmap_ros.

[Install rtabmap and rtabmap_ros](https://github.com/introlab/rtabmap_ros/tree/ros2) by following the tutorial in README.

Install imu tools and navigation2

```bash
sudo apt-get install ros-humble-imu-tools
sudo apt install ros-humble-navigation2
sudo apt install ros-humble-nav2-bringup
sudo apt install ros-humble-apriltag*
```

[Mapping tutorial](http://wiki.ros.org/rtabmap_ros/Tutorials/HandHeldMapping) 

Set numeric locale to US beforehand to stop rtabmap from crashing.

```bash
LC_NUMERIC="en_US.UTF-8"
```

Set it back to Estonian after mapping just in case.

```bash
LC_NUMERIC="et_EE.UTF-8"
```

### Mapping with rtabmap
To start mapping, launch the mapping.launch file. Make sure the params align_depth.enable, enable_gyro and enable_accel are true. unite_imu_method = 1. The odometry tends do drift somewhat when mapping, so make sure to drive slowly. You will notice the rtabmap screen going red if this happens. This is very relevant if you're trying to turn the robot around in a narrow hallway. If it does lose track, try going back a little bit first. Otherwise, use the rtabmap GUI to reset odometry.

```bash
ros2 launch hospital_carrier mapping.launch
```
To save the generated 2D map, run the command below. This needs nav2 stack to be running!

```bash
ros2 run nav2_map_server map_saver_cli -f filepath/filename
```

You can save the point cloud through the rtabmap GUI. Default database location for rtabmap is /.ros/rtabmap.db. 

To start a new instance of mapping, add `arguments=['-d']` to the rtab_slam node in realsense_d435i_color.launch.py. This will overwrite the existing database, so make sure to save it beforehand!

### Navigation with rtabmap

Start the navigation2 stack to navigate. Params are optional.
```bash
ros2 launch nav2_bringup navigation_launch.py params_file:=src/robot_ros2/config/nav2_params.yaml
```

In rviz, give a 2D Pose estimate of where the robot is on the map. Then set a 2D Goal Pose to send it where you want it to go.

To do localization, change the mode in rtabmap GUI to localization.

### Apriltag markers

Place apriltag markers to help localize the robot and fix the odometry when mapping or navigating. Download more images from [this link](https://github.com/AprilRobotics/apriltag-imgs). We use 36h11 type markers that are scaled to 10000% of their original size. All markers have to be from the same family of markers!

## Playstation remote and changing operation mode
The robot currently has 2 modes of movement:
1. Following a line
2. Operated by Playstation4 remote
If the remote is connected to the computer then pressing "PS4" button on it once makes the operation mode switch 
   between "paused" and "PS4 control". Pressing the button twice fast makes the operation mode 
   go to "linefollower" state.
   
To achieve the same without the PS4 remote open another terminal and type one of the following
```bash
ros2 topic pub hospital_carrier/op_mode_change_request std_msgs/String "data: ps4controller-click"
```
```bash
ros2 topic pub hospital_carrier/op_mode_change_request std_msgs/String "data: ps4controller-doubleclick"
```

## ODrive firmware upgrade

To upgrade ODrive firmware, you need to have `odrivetool` installed. As some use cases need sudo access, but normally user access is sufficient, you need to install it using `sudo -H pip install odrive`. (NB! package name is `odrive` and command name `odrivetool`). Now do the following:

1. Update odrivetool to the latest version (e.g. `sudo -H pip install odrive --upgrade`) if it is not already
2. If you have not used your computer before for odrive upgrade, configure udev rules `odrivetool udev-setup` and enable the rules using `sudo udevadm control --reload-rules && sudo udevadm trigger`.
2. Connect Odrive using micro-USB cable using a micro-usb port on odrive (NB! not the USB-UART convertor cable that is used in robot) and power up odrive
3. launch `odrivetool dfu` to start the firmware upgrade


## How to SLAM with slam_toolbox

First make sure you have installed slam-toolbox and navigation2. 

```bash
sudo apt install ros-humble-slam-toolbox
sudo apt install ros-humble-navigation2
sudo apt install ros-humble-nav2-bringup
```

Open 4 terminal windows. 
1. In terminal 1, start the robot nodes

```bash
ros2 launch hospital_carrier hospital_robot.launch
```
2. In terminal 2, start the navigation stack

```bash
ros2 launch nav2_bringup navigation_launch.py
```
3. In terminal 3, start the SLAM functionality

```bash
ros2 launch slam_toolbox online_async_launch.py slam_params_file:=robot_ros2/src/robot_ros2/config/mapper_params_online_async.yaml use_sim_time:=false
```
4. In terminal 4, launch rviz2

```bash
rviz2
```

To launch already made map
```bash
ros2 run nav2_bringup bringup_launch.py map:=path_to_map/map.yaml
```
