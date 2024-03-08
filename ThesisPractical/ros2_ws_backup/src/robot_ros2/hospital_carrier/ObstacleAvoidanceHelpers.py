
class ObstacleAvoidanceHelpers:
    def __init__(self):
        self.road_section_choice_angles = [-0.78, -0.52, -0.26, 0.26, 0.52, 0.78]
        self.segment_turn_radiuses = [1.0, 2.0, 3.0, None, -3.0, -2.0, -1.0] # turn radiuses matching to routes that
                                                                             # ObstacleDetector measures, in m
        self.obstacle_min_distance_to_drive = 1.0
        self.directions_priority_helpers = [1, 2, -1, -2, 3, 4, -3, -4, 5, 6, -5, -6]

        self.max_x_vel = 0.25
        self.space_for_max_x_vel = 1
        self.speeds = [0, 0]
        self.prev_speeds = [0, 0]
        self.lin_max_change = 0.1  # for controlSpeedsByRadius method

    def findBestDirectionFromAngle(self, angle):
        """
        Returns a number 0-6 that denotes a turn radius sector
        """
        best_direction = 6
        for i, val in enumerate(self.road_section_choice_angles):
            if angle < val:
                best_direction = i
                break
        return best_direction

    def findPathToDrive(self, best_direction, obst_dists_on_paths, needed_distance = 0):
        """
        @param best_direction - preferred direction 0-6
        @param obst_dists_on_paths - list of 7 distance values got from LineAndObstacleDetector
        @param needed_distance - set value for this param when doing coordinate navigation
        Returns a number 0-6 that denotes a turn radius sector or -1 if no sector has enough free space.
        """
        if needed_distance == 0:
            needed_distance = self.obstacle_min_distance_to_drive

        # Assemble priority list around best_direction. Smaller angles to the right first, then left,
        # then bigger angles to right etc
        directions_priority_list = [best_direction]

        for c in self.directions_priority_helpers:
            if 0 <= best_direction + c <= 6:
                directions_priority_list.append(best_direction + c)

        # Check in the order of priority if any path is free to drive
        path_to_drive = -1
        for i in directions_priority_list:
            if obst_dists_on_paths[i] > needed_distance:
                path_to_drive = i
                break

        return path_to_drive

    def controlSpeedsByPathToDrive(self, dist_to_obst, path_to_drive):
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
        radius = self.segment_turn_radiuses[path_to_drive]
        if radius is not None:
            self.speeds[1] = self.speeds[0] / radius  # rotational speed in rad

        return self.speeds