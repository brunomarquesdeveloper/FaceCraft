from typing import Any

from .landmarks import POINTS
from .measurements import (
    FaceGeometryError,
    prepare_landmarks,
    point,
)
from .face import measure_face
from .eyes import measure_eyes
from .nose import measure_nose
from .mouth import measure_mouth
from .jaw import measure_jaw
from .eyebrows import measure_eyebrows
from .chin import measure_chin
from .symmetry import measure_symmetry


def calculate_face_geometry(
    landmarks: list[dict[str, Any]],
    image_width: int,
    image_height: int,
) -> dict[str, Any]:
    if not landmarks:
        raise FaceGeometryError("Nenhum landmark foi recebido.")

    points = prepare_landmarks(landmarks, image_width, image_height)

    def p(name):
        return point(points, POINTS[name])

    face = measure_face(p)
    face_height = face["height"]
    cheek_width = face["cheek_width"]

    eyes = measure_eyes(p, face_height, cheek_width)
    nose = measure_nose(p, face_height, cheek_width)
    mouth = measure_mouth(p, face_height, cheek_width)
    jaw = measure_jaw(p, cheek_width)
    eyebrows = measure_eyebrows(p, cheek_width)
    chin = measure_chin(p, face_height, cheek_width)
    symmetry = measure_symmetry(eyes["asymmetry"])

    forehead = p("forehead")
    left_temple = p("left_temple")
    right_temple = p("right_temple")

    checklist = {
        "face": "ok",
        "forehead": (
            "ok" if forehead and left_temple and right_temple
            else "incomplete"
        ),
        "eyes": (
            "ok" if all(value is not None for value in [
                eyes["left_width"], eyes["right_width"],
                eyes["left_height"], eyes["right_height"],
                eyes["interocular"],
            ]) else "incomplete"
        ),
        "eyebrows": (
            "ok" if p("left_brow") and p("right_brow")
            else "incomplete"
        ),
        "nose": (
            "ok" if nose["length"] is not None and nose["width"] is not None
            else "incomplete"
        ),
        "lips": (
            "ok" if all(value is not None for value in [
                mouth["width"], mouth["upper"], mouth["lower"],
            ]) else "incomplete"
        ),
        "jaw": (
            "ok" if all(value is not None for value in [
                jaw["width"], jaw["left_angle"], jaw["right_angle"],
            ]) else "incomplete"
        ),
        "chin": "ok" if p("chin") is not None else "incomplete",
        "cheeks": (
            "ok" if p("left_cheek") and p("right_cheek")
            else "incomplete"
        ),
    }

    return {
        "coordinate_system": {
            "source": "mediapipe_face_landmarker",
            "landmarks_received": len(points),
            "image_width": image_width,
            "image_height": image_height,
            "distance_unit": "pixels",
            "normalized_reference": "cheek_width",
        },
        "capture_checklist": checklist,
        "face": face["data"],
        "forehead": {
            "reference_point": {
                "x": round(forehead["x"], 3) if forehead else None,
                "y": round(forehead["y"], 3) if forehead else None,
            },
            "width_px": None,
            "height_px": None,
            "status": "partially_measured",
        },
        "jaw": jaw["data"],
        "chin": chin["data"],
        "eyes": eyes["data"],
        "nose": nose["data"],
        "mouth": mouth["data"],
        "eyebrows": eyebrows["data"],
        "symmetry": symmetry,
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
