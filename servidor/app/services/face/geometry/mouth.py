from .measurements import distance_2d, rounded, ratio


def measure_mouth(p, face_height, cheek_width):
    width = distance_2d(
        p("left_mouth_corner"),
        p("right_mouth_corner"),
    )
    upper = distance_2d(p("upper_lip_outer"), p("upper_lip_inner"))
    lower = distance_2d(p("lower_lip_inner"), p("lower_lip_outer"))
    opening = distance_2d(p("upper_lip_inner"), p("lower_lip_inner"))
    total_height = distance_2d(
        p("upper_lip_outer"),
        p("lower_lip_outer"),
    )

    return {
        "width": width,
        "upper": upper,
        "lower": lower,
        "total_height": total_height,
        "data": {
            "width_px": rounded(width),
            "width_face_ratio": ratio(width, cheek_width),
            "upper_lip_thickness_px": rounded(upper),
            "lower_lip_thickness_px": rounded(lower),
            "upper_lip_face_ratio": ratio(upper, face_height),
            "lower_lip_face_ratio": ratio(lower, face_height),
            "opening_px": rounded(opening),
            "total_lip_height_px": rounded(total_height),
            "status": (
                "measured" if total_height is not None
                else "partially_measured"
            ),
        },
    }
