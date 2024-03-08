Running the system:

camera/navigation stack:
ros2 launch nav2_bringup navigation_launch.py params_file:=src/robot_ros2/config/nav2_params.yaml

robot:
ros2 launch hospital_carrier hospital_robot.launch


Object detection:
$ ros2 launch yolov8_bringup yolov8_3d.launch.py

segmentation:
ros2 launch yolov8_bringup yolov8_3d.launch.py model:=yolov8m-seg.pt

    or manual remap:
    ros2 launch yolov8_bringup yolov8_3d.launch.py model:=yolov8m-seg.pt input_image_topic:=/camera/color/image_raw input_depth_topic:=/camera/depth/image_rect_raw input_depth_info_topic:=/camera


