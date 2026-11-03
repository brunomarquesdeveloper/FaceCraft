from .measurements import rounded


def measure_symmetry(eye_asymmetry):
    return {
        "eye_width_asymmetry_ratio": rounded(eye_asymmetry, 5),
        "status": "partial",
        "note": (
            "Somente a diferença de largura entre os olhos foi calculada. "
            "Não representa simetria facial completa."
        ),
    }
