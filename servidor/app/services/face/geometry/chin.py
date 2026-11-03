from .measurements import rounded, ratio


def measure_chin(p, face_height, cheek_width):
    chin = p("chin")
    forehead = p("forehead")
    left_cheek = p("left_cheek")
    right_cheek = p("right_cheek")

    center_x = None
    if left_cheek is not None and right_cheek is not None:
        center_x = (left_cheek["x"] + right_cheek["x"]) / 2

    x_centered_ratio = None
    y_face_ratio = None

    if chin is not None and center_x is not None:
        x_centered_ratio = ratio(chin["x"] - center_x, cheek_width)

    if chin is not None and forehead is not None:
        y_face_ratio = ratio(chin["y"] - forehead["y"], face_height)

    return {
        "data": {
            "position": {
                "x": rounded(chin["x"] if chin else None),
                "y": rounded(chin["y"] if chin else None),
                "x_centered_ratio": x_centered_ratio,
                "y_face_ratio": y_face_ratio,
            },
            "width_px": None,
            "status": "partially_measured",
        },
    }
