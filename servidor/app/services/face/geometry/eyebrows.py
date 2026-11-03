from .measurements import distance_2d, ratio, rounded


def measure_eyebrows(p, cheek_width):
    distance = distance_2d(p("left_brow"), p("right_brow"))

    return {
        "distance": distance,
        "data": {
            "distance_px": rounded(distance),
            "distance_face_ratio": ratio(distance, cheek_width),
            "status": "measured" if distance is not None else "not_measured",
        },
    }
