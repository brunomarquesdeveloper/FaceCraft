from .measurements import distance_2d, ratio, rounded


def measure_face(p):
    forehead = p("forehead")
    chin = p("chin")
    left_cheek = p("left_cheek")
    right_cheek = p("right_cheek")
    left_temple = p("left_temple")
    right_temple = p("right_temple")
    left_jaw = p("left_jaw")
    right_jaw = p("right_jaw")

    height = distance_2d(forehead, chin)
    cheek_width = distance_2d(left_cheek, right_cheek)
    temple_width = distance_2d(left_temple, right_temple)
    jaw_width = distance_2d(left_jaw, right_jaw)

    if height is None or cheek_width is None:
        raise ValueError(
            "Landmarks insuficientes para calcular as proporções faciais."
        )

    if height <= 0 or cheek_width <= 0:
        raise ValueError("Geometria facial inválida.")

    return {
        "height": height,
        "cheek_width": cheek_width,
        "data": {
            "height_px": rounded(height),
            "cheek_width_px": rounded(cheek_width),
            "temple_width_px": rounded(temple_width),
            "jaw_width_px": rounded(jaw_width),
            "width_height_ratio": ratio(cheek_width, height),
            "temple_width_ratio": ratio(temple_width, cheek_width),
            "jaw_width_ratio": ratio(jaw_width, cheek_width),
        },
    }
