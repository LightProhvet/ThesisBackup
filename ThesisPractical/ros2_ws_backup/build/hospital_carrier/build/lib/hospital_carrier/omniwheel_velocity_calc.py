def joysticks_to_velocities(lx, ly, rx):
    scale = 100000

    # lx and ly determine translation,
    # rx determines pure rotation.

    # For the theory, see https://web.archive.org/web/20181228164431/https://www.chiefdelphi.com/media/papers/download/2614

    angular_coeff = -1

    v_front_left = ly + lx - angular_coeff * rx
    v_front_right = ly - lx + angular_coeff * rx
    v_rear_left = ly - lx - angular_coeff * rx
    v_rear_right = ly + lx + angular_coeff * rx

    v_axes = (v_rear_left, v_front_left, -v_front_right, -v_rear_right)

    return (scale * v for v in v_axes)
