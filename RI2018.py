def reward_function(params):
    fast_area = [25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 42]

    str_line = [43, 44, 45, 46, 47, 48, 49,
                54, 55, 56, 57, 58, 59, 60,
                68, 69, 70, 71, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

    ninety_corner = [50, 51, 52, 53,
                     61, 62, 63, 64, 65, 66, 67]
    large_corner = [10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24]

    heading = params['heading']
    closest_waypoints = params['closest_waypoints']
    is_left_of_center = params['is_left_of_center']
    speed = params["speed"]
    is_offtrack = params["is_offtrack"]
    progress = params["progress"]
    steps = params["steps"]
    track_width = params['track_width']
    distance_from_center = params['distance_from_center']
    track_side_1 = 0.5 * track_width
    track_side_2 = 0.4 * track_width
    track_side_3 = 0.3 * track_width

    left_lane_factor = 0
    if is_left_of_center:
        left_lane_factor = 10

    if closest_waypoints[1] in fast_area:
        heading_factor = 1
        if 145 < heading < 155:
            heading_factor = 10
        elif 130 < heading < 160:
            heading_factor = 5

        speed_factor = 1
        if speed > 3:
            speed_factor = 10
        elif speed > 2:
            speed_factor = 5

        if not is_offtrack:
            reward = heading_factor * speed_factor
        else:
            reward = 0.01

    elif closest_waypoints[1] in str_line:
        speed_factor = 1
        if speed > 2:
            speed_factor = 10
        elif speed > 1:
            speed_factor = 5

        if not is_offtrack:
            reward = (progress / steps) * (speed_factor ** 2)
        else:
            reward = 0.01
    elif closest_waypoints[1] in ninety_corner:
        speed_factor = 1
        if 1.5 < speed < 2.2:
            speed_factor = 10
        elif 0.8 < speed < 1.5:
            speed_factor = 5

        if not is_offtrack:
            reward = left_lane_factor * speed_factor
        else:
            reward = 0.01

    elif closest_waypoints[1] in large_corner:
        track_side_factor = 1
        if track_side_2 < distance_from_center <= track_side_1:
            track_side_factor = 10
        elif track_side_3 < distance_from_center <= track_side_1:
            track_side_factor = 5

        speed_factor = 1
        if 0.8 < speed <= 1:
            speed_factor = 10
        elif 0.5 < speed <= 0.8:
            speed_factor = 5

        if not is_offtrack and is_left_of_center:
            reward = track_side_factor * speed_factor
        else:
            reward = 0.01

    else:
        if params["all_wheels_on_track"] and params["steps"] > 0:
            reward = ((params["progress"] / params["steps"]) * 100) + (params["speed"] ** 2)
        else:
            reward = 0.01

    return float(reward)
