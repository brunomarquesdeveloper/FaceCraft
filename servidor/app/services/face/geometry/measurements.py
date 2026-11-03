from __future__ import annotations

from math import atan2, degrees, hypot
from typing import Any


class FaceGeometryError(Exception):
    """Erro ao calcular a geometria facial."""


def prepare_landmarks(
    landmarks: list[dict[str, Any]],
    image_width: int,
    image_height: int,
) -> dict[int, dict[str, float]]:
    if image_width <= 0 or image_height <= 0:
        raise FaceGeometryError("Dimensões da imagem inválidas.")

    points = {}

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


def point(points, index):
    return points.get(index)


def distance_2d(a, b):
    if a is None or b is None:
        return None

    return hypot(a["x"] - b["x"], a["y"] - b["y"])


def ratio(numerator, denominator):
    if numerator is None or denominator is None or denominator <= 0:
        return None

    return round(numerator / denominator, 5)


def rounded(value, digits=3):
    return round(value, digits) if value is not None else None


def angle_degrees(a, vertex, b):
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
