from .measurements import distance_2d, ratio, angle_degrees, rounded


def measure_jaw(p, cheek_width):
    left_cheek = p("left_cheek")
    right_cheek = p("right_cheek")
    left_jaw = p("left_jaw")
    right_jaw = p("right_jaw")
    chin = p("chin")

    width = distance_2d(left_jaw, right_jaw)
    left_angle = angle_degrees(left_cheek, left_jaw, chin)
    right_angle = angle_degrees(right_cheek, right_jaw, chin)

    return {
        "width": width,
        "left_angle": left_angle,
        "right_angle": right_angle,
        "data": {
            "width_px": rounded(width),
            "width_ratio": ratio(width, cheek_width),
            "left_angle_degrees": left_angle,
            "right_angle_degrees": right_angle,
        },
    }
