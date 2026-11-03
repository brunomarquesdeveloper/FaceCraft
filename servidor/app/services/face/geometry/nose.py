from .measurements import distance_2d, rounded, ratio


def measure_nose(p, face_height, cheek_width):
    bridge = p("nose_bridge")
    tip = p("nose_tip")

    length = distance_2d(bridge, tip)
    width = distance_2d(p("left_nostril"), p("right_nostril"))

    depth = None
    if bridge is not None and tip is not None:
        depth = tip["z"] - bridge["z"]

    return {
        "length": length,
        "width": width,
        "data": {
            "length_px": rounded(length),
            "width_px": rounded(width),
            "length_face_ratio": ratio(length, face_height),
            "width_face_ratio": ratio(width, cheek_width),
            "depth_difference_relative": rounded(depth, 5),
            "depth_source": "mediapipe_relative_z_estimate",
            "depth_status": "estimated",
        },
    }
