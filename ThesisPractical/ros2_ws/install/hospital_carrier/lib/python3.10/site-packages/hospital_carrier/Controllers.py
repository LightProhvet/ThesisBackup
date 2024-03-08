#!/usr/bin/env python

"""
@author: Christian Meurer
"""

import numpy as np
from geometry_msgs.msg import Vector3Stamped

class Controller:
    def control(self, error):
        """
        @param error - error in planar position and orientation -
            [x, y, yaw] in local frame
        """
        return np.zeros(3)

class PIDController:
    def __init__(self, dt):
        self.dt = dt

        self.max_x_vel = 0.25
        self.space_for_max_x_vel = 1

        self.Kp = np.zeros([3])
        self.Ki = np.zeros([3])
        self.Kd = np.zeros([3])

        self.windup_limit = np.array([0.1, 0.1, 0.1])

        self.last_error = np.zeros(3)
        self.int_error = np.zeros(3)

        self.speeds = [0, 0]
        self.prev_speeds = [0, 0]
        self.lin_max_change = 0.02  # for control_by_radius method


    def setGains(self, mode):
        if mode == "Omni":
            self.Kp = np.array([1.0, 0.0, 0.5])
            self.Ki = np.array([0.0, 0.0, 0.05])
            self.Kd = np.array([0.0, 0.0, 0.3])
            
        elif mode == "Diff":
            self.Kp = np.array([0.0, 0.0, 0.0])
            self.Ki = np.array([0.0, 0.0, 0.0])
            self.Kd = np.array([0.0, 0.0, 0.0])

    def control(self, line_error):
        # line_error[0] - distance in mm in X direction
        # line_error[1] - distance in mm in Y direction
        # line_error[2] - difference in rad (measurement center point is front of robot not center of robot)

        destination_error = np.array([
            line_error[0]/self.space_for_max_x_vel,
            0,   # Y movement currently not in use
            line_error[2]
        ], dtype=float)
        if destination_error[0] > 1:
            destination_error[0] = 1

        d_error = (self.last_error - destination_error) / self.dt

        self.int_error = np.clip(self.int_error + destination_error * self.dt,
                                 -self.windup_limit, self.windup_limit)

        pid = self.Kp * destination_error + self.Ki * self.int_error + self.Kd * d_error

        # Map x direction speed to vel_x_const parameter.
        pid[0] = pid[0] * self.max_x_vel

        if pid[2] < 0.25:  # Dirty fix for too sudden rotation moves
            pid[2] = 0.25

        self.last_error = destination_error
        self.speeds[0] = pid[0]
        self.speeds[1] = pid[2]

        #self.get_logger().info("PID input", line_error[0], line_error[2], " Output:", pid[0], pid[2])
        return pid


    def control_by_radius(self, dist_to_obst, radius):  #dist to obst, radius in m or None
        self.prev_speeds = self.speeds
        self.speeds[0] = 0
        self.speeds[1] = 0
        speed_coef = dist_to_obst / self.space_for_max_x_vel
        if speed_coef > 1:
            speed_coef = 1
        self.speeds[0] = speed_coef * self.max_x_vel
        if self.speeds[0] > self.prev_speeds[0] + self.lin_max_change:
            self.speeds[0] = self.lin_max_change
        # Not limiting deceleration on purpose

        if radius is not None:
            self.speeds[1] = self.speeds[0] / radius  # rotational speed in rad

        return self.speeds




class CoordNavController:
    def __init__(self, max_lin_speed, min_lin_speed, max_rot_speed, min_rot_speed, linear_proportional_div,
                 rot_proportional_div, lin_max_change):
        self.speeds = [0, 0]
        self.prev_speeds = [0, 0]
        self.max_linear = max_lin_speed
        self.min_linear = min_lin_speed
        self.max_rot = max_rot_speed
        self.min_rot = min_rot_speed
        self.lin_proportion = linear_proportional_div
        self.rot_proportion = rot_proportional_div
        self.lin_max_change = lin_max_change

    def control(self, lin_dist, rotation_diff):  # lin_dist in m, rotation diff in rad
        linear = lin_dist * self.lin_proportion  # speed m/s
        if linear > self.max_linear:
            linear = self.max_linear
        elif linear < -1 * self.max_linear:  # negative speeds should not happen, but just for safety...
            linear = -1 * self.max_linear / 10
        elif self.min_linear > linear > 0:
            linear = self.min_linear
        elif -1*self.min_linear < linear < 0:
            linear = -1*self.min_linear
        lin_diff = linear - self.speeds[0]
        if lin_diff > self.lin_max_change:
            linear = self.speeds[0] + self.lin_max_change
        elif lin_diff < -1 * self.lin_max_change:
            linear = self.speeds[0] - self.lin_max_change

        rot = rotation_diff * self.rot_proportion
        if rot > self.max_rot:
            rot = self.max_rot
        elif rot < -1 * self.max_rot:
            rot = -1 * self.max_rot
        elif self.min_rot > rot > 0:
            rot = self.min_rot
        elif -1*self.min_rot < rot < 0:
            rot = -1*self.min_rot

        self.prev_speeds = self.speeds
        self.speeds[0] = linear
        self.speeds[1] = rot

        return self.speeds
