
from __future__ import annotations

from math import atan2, degrees, hypot
from typing import Any


# Índices canônicos do MediaPipe Face Mesh.
# Referências geométricas aproximadas, não medidas clínicas.
POINTS = {
    "forehead": 10,
    "chin": 152,

    "left_cheek": 234,
    "right_cheek": 454,

    "left_temple": 127,
    "right_temple": 356,

    "left_jaw": 172,
    "right_jaw": 397,

    "left_eye_outer": 33,
    "left_eye_inner": 133,
    "left_eye_upper": 159,
    "left_eye_lower": 145,

    "right_eye_inner": 362,
    "right_eye_outer": 263,
    "right_eye_upper": 386,
    "right_eye_lower": 374,

    "left_brow": 105,
    "right_brow": 334,

    "nose_bridge": 168,
    "nose_tip": 1,
    "left_nostril": 98,
    "right_nostril": 327,

    "left_mouth_corner": 61,
    "right_mouth_corner": 291,

    "upper_lip_outer": 0,
    "upper_lip_inner": 13,
    "lower_lip_inner": 14,
    "lower_lip_outer": 17,
}


class FaceGeometryError(Exception):
    """Erro ao calcular a geometria facial."""


def _prepare_landmarks(
    landmarks: list[dict[str, Any]],
    image_width: int,
    image_height: int,
) -> dict[int, dict[str, float]]:

    if image_width <= 0 or image_height <= 0:
        raise FaceGeometryError("Dimensões da imagem inválidas.")

    points: dict[int, dict[str, float]] = {}

    for landmark in landmarks:
        try:
            index = int(landmark["index"])
            x = float(landmark["x"])
            y = float(landmark["y"])
            z = float(landmark.get("z", 0.0))

            if not all(
                value == value and abs(value) != float("inf")
                for value in (x, y, z)
            ):
                continue

        except (KeyError, TypeError, ValueError):
            continue

        points[index] = {
            "x": x * image_width,
            "y": y * image_height,
            "z": z * image_width,
        }

    return points


def _point(
    points: dict[int, dict[str, float]],
    index: int,
) -> dict[str, float] | None:

    return points.get(index)


def _distance_2d(
    a: dict[str, float] | None,
    b: dict[str, float] | None,
) -> float | None:

    if a is None or b is None:
        return None

    return hypot(
        a["x"] - b["x"],
        a["y"] - b["y"],
    )


def _ratio(
    numerator: float | None,
    denominator: float | None,
) -> float | None:

    if numerator is None or denominator is None:
        return None

    if denominator <= 0:
        return None

    return round(numerator / denominator, 5)


def _round(
    value: float | None,
    digits: int = 3,
) -> float | None:

    if value is None:
        return None

    return round(value, digits)


def _angle_degrees(
    a: dict[str, float] | None,
    vertex: dict[str, float] | None,
    b: dict[str, float] | None,
) -> float | None:
    """Calcula o ângulo geométrico 2D entre três landmarks."""

    if a is None or vertex is None or b is None:
        return None

    angle_a = atan2(
        a["y"] - vertex["y"],
        a["x"] - vertex["x"],
    )

    angle_b = atan2(
        b["y"] - vertex["y"],
        b["x"] - vertex["x"],
    )

    difference = abs(degrees(angle_a - angle_b))

    return round(min(difference, 360 - difference), 2)


def calculate_face_geometry(
    landmarks: list[dict[str, Any]],
    image_width: int,
    image_height: int,
) -> dict[str, Any]:
    """
    Calcula as características geométricas do rosto.

    Retorna:
    - Medidas faciais em pixels.
    - Proporções normalizadas.
    - Estimativas relativas.
    - Checklist de captura por região facial.

    Não interpreta expressões faciais.
    Não inventa medidas ausentes.
    """

    if not landmarks:
        raise FaceGeometryError("Nenhum landmark foi recebido.")

    points = _prepare_landmarks(
        landmarks,
        image_width,
        image_height,
    )

    def p(name: str) -> dict[str, float] | None:
        return _point(points, POINTS[name])

    # ---------------------------------------------------------
    # REFERÊNCIAS FACIAIS
    # ---------------------------------------------------------

    forehead = p("forehead")
    chin = p("chin")

    left_cheek = p("left_cheek")
    right_cheek = p("right_cheek")

    left_temple = p("left_temple")
    right_temple = p("right_temple")

    left_jaw = p("left_jaw")
    right_jaw = p("right_jaw")

    face_height = _distance_2d(forehead, chin)
    cheek_width = _distance_2d(left_cheek, right_cheek)
    temple_width = _distance_2d(left_temple, right_temple)
    jaw_width = _distance_2d(left_jaw, right_jaw)

    if face_height is None or cheek_width is None:
        raise FaceGeometryError(
            "Landmarks insuficientes para calcular as proporções faciais."
        )

    if face_height <= 0 or cheek_width <= 0:
        raise FaceGeometryError("Geometria facial inválida.")

    # ---------------------------------------------------------
    # OLHOS
    # ---------------------------------------------------------

    left_eye_width = _distance_2d(
        p("left_eye_outer"),
        p("left_eye_inner"),
    )

    right_eye_width = _distance_2d(
        p("right_eye_inner"),
        p("right_eye_outer"),
    )

    left_eye_height = _distance_2d(
        p("left_eye_upper"),
        p("left_eye_lower"),
    )

    right_eye_height = _distance_2d(
        p("right_eye_upper"),
        p("right_eye_lower"),
    )

    left_eye_center = None
    right_eye_center = None

    if p("left_eye_outer") and p("left_eye_inner"):
        a = p("left_eye_outer")
        b = p("left_eye_inner")

        left_eye_center = {
            "x": (a["x"] + b["x"]) / 2,
            "y": (a["y"] + b["y"]) / 2,
        }

    if p("right_eye_outer") and p("right_eye_inner"):
        a = p("right_eye_outer")
        b = p("right_eye_inner")

        right_eye_center = {
            "x": (a["x"] + b["x"]) / 2,
            "y": (a["y"] + b["y"]) / 2,
        }

    interocular_distance = _distance_2d(
        left_eye_center,
        right_eye_center,
    )

    eye_width_asymmetry = None

    if (
        left_eye_width is not None
        and right_eye_width is not None
        and max(left_eye_width, right_eye_width) > 0
    ):
        eye_width_asymmetry = (
            abs(left_eye_width - right_eye_width)
            / max(left_eye_width, right_eye_width)
        )

    # ---------------------------------------------------------
    # NARIZ
    # ---------------------------------------------------------

    nose_length = _distance_2d(
        p("nose_bridge"),
        p("nose_tip"),
    )

    nose_width = _distance_2d(
        p("left_nostril"),
        p("right_nostril"),
    )

    nose_depth_relative = None

    if p("nose_bridge") and p("nose_tip"):
        nose_depth_relative = (
            p("nose_tip")["z"] - p("nose_bridge")["z"]
        )

    # ---------------------------------------------------------
    # BOCA E LÁBIOS
    # ---------------------------------------------------------

    mouth_width = _distance_2d(
        p("left_mouth_corner"),
        p("right_mouth_corner"),
    )

    upper_lip_thickness = _distance_2d(
        p("upper_lip_outer"),
        p("upper_lip_inner"),
    )

    lower_lip_thickness = _distance_2d(
        p("lower_lip_inner"),
        p("lower_lip_outer"),
    )

    mouth_opening = _distance_2d(
        p("upper_lip_inner"),
        p("lower_lip_inner"),
    )

    total_lip_height = _distance_2d(
        p("upper_lip_outer"),
        p("lower_lip_outer"),
    )

    # ---------------------------------------------------------
    # MANDÍBULA
    # ---------------------------------------------------------

    left_jaw_angle = _angle_degrees(
        left_cheek,
        left_jaw,
        chin,
    )

    right_jaw_angle = _angle_degrees(
        right_cheek,
        right_jaw,
        chin,
    )

    # ---------------------------------------------------------
    # SOBRANCELHAS
    # ---------------------------------------------------------

    brow_distance = _distance_2d(
        p("left_brow"),
        p("right_brow"),
    )

    # ---------------------------------------------------------
    # CHECKLIST DE CAPTURA
    # ---------------------------------------------------------

    capture_checklist = {
        "face": (
            "ok"
            if face_height is not None and cheek_width is not None
            else "incomplete"
        ),

        "forehead": (
            "ok"
            if (
                forehead is not None
                and left_temple is not None
                and right_temple is not None
            )
            else "incomplete"
        ),

        "eyes": (
            "ok"
            if all(value is not None for value in [
                left_eye_width,
                right_eye_width,
                left_eye_height,
                right_eye_height,
                interocular_distance,
            ])
            else "incomplete"
        ),

        "eyebrows": (
            "ok"
            if (
                p("left_brow") is not None
                and p("right_brow") is not None
            )
            else "incomplete"
        ),

        "nose": (
            "ok"
            if (
                nose_length is not None
                and nose_width is not None
            )
            else "incomplete"
        ),

        "lips": (
            "ok"
            if all(value is not None for value in [
                mouth_width,
                upper_lip_thickness,
                lower_lip_thickness,
            ])
            else "incomplete"
        ),

        "jaw": (
            "ok"
            if all(value is not None for value in [
                jaw_width,
                left_jaw_angle,
                right_jaw_angle,
            ])
            else "incomplete"
        ),

        "chin": (
            "ok"
            if chin is not None
            else "incomplete"
        ),

        "cheeks": (
            "ok"
            if (
                left_cheek is not None
                and right_cheek is not None
                and cheek_width is not None
            )
            else "incomplete"
        ),
    }

    # ---------------------------------------------------------
    # RESULTADO
    # ---------------------------------------------------------

    return {
        "coordinate_system": {
            "source": "mediapipe_face_landmarker",
            "landmarks_received": len(points),
            "image_width": image_width,
            "image_height": image_height,
            "distance_unit": "pixels",
            "normalized_reference": "cheek_width",
        },

        "capture_checklist": capture_checklist,

        "face": {
            "height_px": _round(face_height),
            "cheek_width_px": _round(cheek_width),
            "temple_width_px": _round(temple_width),
            "jaw_width_px": _round(jaw_width),

            "width_height_ratio": _ratio(
                cheek_width,
                face_height,
            ),

            "temple_width_ratio": _ratio(
                temple_width,
                cheek_width,
            ),

            "jaw_width_ratio": _ratio(
                jaw_width,
                cheek_width,
            ),
        },

        "forehead": {
            "reference_point": {
                "x": _round(forehead["x"] if forehead else None),
                "y": _round(forehead["y"] if forehead else None),
            },
            "width_px": None,
            "height_px": None,
            "status": "partially_measured",
        },

        "jaw": {
            "width_px": _round(jaw_width),

            "width_ratio": _ratio(
                jaw_width,
                cheek_width,
            ),

            "left_angle_degrees": left_jaw_angle,
            "right_angle_degrees": right_jaw_angle,
        },

        "chin": {
            "position": {
                "x": _round(chin["x"] if chin else None),
                "y": _round(chin["y"] if chin else None),
            },
            "width_px": None,
            "status": "partially_measured",
        },

        "eyes": {
            "left": {
                "width_px": _round(left_eye_width),
                "height_px": _round(left_eye_height),

                "width_face_ratio": _ratio(
                    left_eye_width,
                    cheek_width,
                ),

                "height_face_ratio": _ratio(
                    left_eye_height,
                    face_height,
                ),
            },

            "right": {
                "width_px": _round(right_eye_width),
                "height_px": _round(right_eye_height),

                "width_face_ratio": _ratio(
                    right_eye_width,
                    cheek_width,
                ),

                "height_face_ratio": _ratio(
                    right_eye_height,
                    face_height,
                ),
            },

            "interocular_distance_px": _round(
                interocular_distance
            ),

            "interocular_distance_ratio": _ratio(
                interocular_distance,
                cheek_width,
            ),

            "width_asymmetry_ratio": _round(
                eye_width_asymmetry,
                5,
            ),
        },

        "nose": {
            "length_px": _round(nose_length),
            "width_px": _round(nose_width),

            "length_face_ratio": _ratio(
                nose_length,
                face_height,
            ),

            "width_face_ratio": _ratio(
                nose_width,
                cheek_width,
            ),

            "depth_difference_relative": _round(
                nose_depth_relative,
                5,
            ),

            "depth_source": "mediapipe_relative_z_estimate",
            "depth_status": "estimated",
        },

        "mouth": {
            "width_px": _round(mouth_width),

            "width_face_ratio": _ratio(
                mouth_width,
                cheek_width,
            ),

            "upper_lip_thickness_px": _round(
                upper_lip_thickness
            ),

            "lower_lip_thickness_px": _round(
                lower_lip_thickness
            ),

            "opening_px": _round(mouth_opening),

            "total_lip_height_px": _round(
                total_lip_height
            ),

            "status": (
                "measured"
                if total_lip_height is not None
                else "partially_measured"
            ),
        },

        "eyebrows": {
            "distance_px": _round(brow_distance),

            "status": (
                "measured"
                if brow_distance is not None
                else "not_measured"
            ),
        },

        "symmetry": {
            "eye_width_asymmetry_ratio": _round(
                eye_width_asymmetry,
                5,
            ),

            "status": "partial",

            "note": (
                "Somente a diferença de largura entre os olhos "
                "foi calculada. Não representa simetria facial completa."
            ),
        },

        "measurement_notes": [
            "As medidas em pixels representam distâncias na fotografia.",
            "As proporções são normalizadas pela largura das maçãs do rosto ou altura facial.",
            "O Z do MediaPipe é relativo e não representa profundidade física.",
            "Os ângulos mandibulares são aproximações geométricas.",
            "As medidas dos lábios são aproximações entre landmarks.",
            "A simetria completa ainda não foi implementada.",
            "Nenhuma medida ausente é substituída por um valor inventado.",
        ],
    }
