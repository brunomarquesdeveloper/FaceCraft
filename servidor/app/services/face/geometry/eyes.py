from .measurements import distance_2d, ratio, rounded


def measure_eyes(p, face_height, cheek_width):
    left_width = distance_2d(p("left_eye_outer"), p("left_eye_inner"))
    right_width = distance_2d(p("right_eye_inner"), p("right_eye_outer"))

    left_height = distance_2d(p("left_eye_upper"), p("left_eye_lower"))
    right_height = distance_2d(p("right_eye_upper"), p("right_eye_lower"))

    left_outer, left_inner = p("left_eye_outer"), p("left_eye_inner")
    right_inner, right_outer = p("right_eye_inner"), p("right_eye_outer")

    left_center = None
    right_center = None

    if left_outer and left_inner:
        left_center = {
            "x": (left_outer["x"] + left_inner["x"]) / 2,
            "y": (left_outer["y"] + left_inner["y"]) / 2,
        }

    if right_inner and right_outer:
        right_center = {
            "x": (right_inner["x"] + right_outer["x"]) / 2,
            "y": (right_inner["y"] + right_outer["y"]) / 2,
        }

    interocular = distance_2d(left_center, right_center)

    asymmetry = None
    if (
        left_width is not None
        and right_width is not None
        and max(left_width, right_width) > 0
    ):
        asymmetry = abs(left_width - right_width) / max(
            left_width, right_width
        )

    return {
        "left_width": left_width,
        "right_width": right_width,
        "left_height": left_height,
        "right_height": right_height,
        "interocular": interocular,
        "asymmetry": asymmetry,
        "data": {
            "left": {
                "width_px": rounded(left_width),
                "height_px": rounded(left_height),
                "width_face_ratio": ratio(left_width, cheek_width),
                "height_face_ratio": ratio(left_height, face_height),
            },
            "right": {
                "width_px": rounded(right_width),
                "height_px": rounded(right_height),
                "width_face_ratio": ratio(right_width, cheek_width),
                "height_face_ratio": ratio(right_height, face_height),
            },
            "interocular_distance_px": rounded(interocular),
            "interocular_distance_ratio": ratio(interocular, cheek_width),
            "width_asymmetry_ratio": rounded(asymmetry, 5),
        },
    }
