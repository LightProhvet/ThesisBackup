# Hospital carrier robot platform ROS code overview

Anna Jõgi, January 2022


## Robot’s physical properties and their consequences

**1. Movement.**
Even though the robot is built with meccanum wheels the code mostly uses only x linear and z rotational movements. 
Reason being that one Realsense camera can only detect obstacles in “front” of the robot and moving to other directions would be dangerous. 
In some formulas (odometry) in the code y linear movement is accounted for, but those parts of the code are not fully tested.

**2. Vision and obstacle detection.**
Single RealSense D435 depth and color camera is the only sensor on the robot. Currently exact mounting height and angle of the camera are given as constants to the code and steady relation between camera and the floor’s plane is assumed (environment should not contain sloped floors or downward stairs). 
Camera is mounted relatively high and pointed down to floor just in front of robot, therefore there is negligible blind area between the image and lower part of robot’s body front. 
Higher up the camera sees smaller section and at human head height none of the environment. But assuming obstacles are most likely approximately same width on the floor than higher up (standing humans, open doors, furniture) and not protruding from walls, it’s most important to observe the floor.


## Obstacle and line detection
Image is processed in the following manner:
1. At startup the camera height and angle constants are used to determine distance of floor for each pixel in the depth image. The image has negligible distortion, therefore distance is calculated solely from trigonometric formulas.  
2. Realsense camera node publishes two versions of depth image - full range and aligned to color image. The aligned to color depth image is used for all actions.  
3. Incoming depth image is compared to the calculated floor distances and a mask image is created that covers everything protruding closer than the expected floor, therefore those areas have to be other objects.  
4. For line detection the mask image is overlaid to the color image and then color based detection of line is done effectively only on floor surface.  
5. For obstacles distance detection in the depth image the floor surface is changed into values of great distance. Same is done to pixels with value 0 that occur where distance measurement did not succeed because of the limitations of stereo imaging. The rest of the pixels that were measured successfully are put through a formula that according to their position in the 2D image calculates their distance from the robot’s front plane. Those values are effectively comparable obstacles distances.


## ROS nodes that make up the robot’s behavioural logic

***OperationModeControl node***  
Decides which other node has permission to give velocity commands. Publishes on topic op_mode a name of the node that is allowed to take control or “paused” or “disabled” according to Odrives status and other nodes requests. 
Each node that needs to send velocity commands has to listen to this topic and publish commands ONLY IF the latest op_mode value was it’s name.

***ReadAruco.py***  
Called by LineAndObstacleDetector node. Searches for a known aruco tag in the camera imeage. If found, broadcasts sensor_calculated_camera_link TF2 transform in the aruco’s frame.

***Localizer node***  
Calculates and broadcasts a TF2 transform of:
base_footrpint in odom frame based on velocity command that was executed.
odom in world frame based on sensor_calculated_base_footrprint location when it’s broadcasted as a child of an aruco tag seen in camera, so that base_footrpint would match the location of sensor_calculated_base_footrprint in world

***Follower node***  
In follower mode the robot moves forward guided by line on the floor, obstacles in view and finally robot’s known location and orientation on the map while line is not visible or might be not the line that needs to be followed.

***CoordinateNavigator node***  
In coordinate_navigator mode the robot drives to a location defined by coordinates in 3 steps. First step is to rotate to aim itself facing towards the goal. Second step is to drive towards the goal, adjusting the direction if needed and avoiding obstacles. Third step is to rotate to orient the robot the same as the quaternion of the coordinate location is set. This method of navigation is used for choosing the right exit from a lines crossroad, parking in the destination and for entering and exiting the elevator.

***MqttRemoteControl node***  
Publishes a velocity command if user pushed a movement button in UI. (Mediated by MqttListener node.)  

***PS4Controller node***  
Receives signal from Playstation remote control device. If home button on the remote is pushed, publishes a operation mode change request. If operation mode is PS¤ then publishes velocity commands according to the remote control joystick signals (uses both x and y linear movement and rotation).

***Controllers.py***  
Helpers for calculating body velocity.

***Odrives node***  
Listens to velocity command topic and controls Odrive motor drivers accordingly.


## Static mapping of the environment

TODO

## Communications with web UI
***MqttRemoteControl node***  
Publishes a velocity command if user pushed a movement button in UI. (Mediated by MqttListener node.)

***MqttVideoStreamer node***  
Sends video stream to UI.

## Relevant ROS topics
List of ROS topics that are relevant for robot’s operation. With information which nodes currently exchange information on the topic and explanations for some topic’s functions.

/camera/aligned_depth_to_color/image_raw
Realsense -> LineAndObstacleDetector
Used for distinguishing floor form other objects and calculating horizontal distance to those other objects. 

/camera/color/image_raw
Realsense -> LineAndObstacleDetector / ReadAruco
Used for searching for line and aruco markers. Position of the camera in respect to aruco marker is calculated and robot’s position derived from it.

/cmd_vel
OperationModeControl / Follower / CoordinateNavigator / PS4Controller / MqttRemoteControl -> Odrives
Robot’s movement is controlled through this topic. Note: Nodes take turns controlling motors guided by op_mode topic content. Except for now MqttRemoteControl that publishes irrespective of op_mode.

/hospital_carrier/arucoTag            
ReadAruco -> RouteControl/Localizer/MqttOdomAndStatus
Aruco tag id that was detected in camera image.

/hospital_carrier/battery_voltage
Odrives -> OperationModeControl

/hospital_carrier/camera_stream2
LineAndObstacleDetector -> MqttVideoStreamer
Unmodified camera image forwarded to UI.

/hospital_carrier/cmd_vel_executed
Odrives -> Localizer 
Odrives node is slower at fulfilling move commands than nodes that send them. Only fulfilled commands get forwarded to this topic and can be used for odometry calculations.

/hospital_carrier/coordinate_destination
RouteControl -> CoordinateNavigator
Destination coordinate values for CoordinateNavigator node.

/hospital_carrier/coordinate_navigator_move_complete
CoordinateNavigator -> RouteControl

/hospital_carrier/line_and_obst
LineAndObstDetector -> Follower
Contains z rotation in arbitary unit and x distance of the detected line.
        
/hospital_carrier/motor_cmd
PS4Controller -> Odrives

/hospital_carrier/mqtt_destination_cancel
Not implemented yet

/hospital_carrier/mqtt_destination_command
MqttListener -> RouteControl

/hospital_carrier/mqtt_remote_control_move    
MqttListener -> MqttRemoteControl

/hospital_carrier/obst_dists_on_paths
LineAndObstacleDetector -> CoordNav / Follower

/hospital_carrier/obst_pass_side
LineAndObstacleDetector -> Follower

/hospital_carrier/odrive_errors

/hospital_carrier/odrive_status

/hospital_carrier/op_mode
OperationModeControl -> Follower / CoordinateNavigator / PS4Controller
Nodes that want to publish to vel_cmd topic are allowed to do it only when the latest value in op_mode topic matches the node’s name. This way the robot is controlled by only one node.

/hospital_carrier/op_mode_change_request
… -> OperationModeControl
To switch between different nodes controlling the robot movement, a request has to be published to this topic, then OperationModeControl will change the op_mode if possible.

/hospital_carrier/request_to_server
Not yet implemented, meant for elevator actions

/hospital_carrier/route_finished
RouteControl -> MqttOdomAndStatus

/hospital_carrier/route_started
RouteControl -> MqttOdomAndStatus

/hospital_carrier/server_elevator_open
Not yet implemented

/hospital_carrier/tag_type
Not yet implemented


## Launch files

***hospital_robot.launch*** - The main launch with all features.
***drive.launch*** – Launches nodes that are only needed to drive the robot with a PS4 controller
***mapping.launch*** – Launches nodes needed to perform SLAM with rtabmap