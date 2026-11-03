from __future__ import annotations

import numpy as np


def extract_landmarks(face_landmarks) -> list[dict]:
    """Extrai os pontos faciais em coordenadas normalizadas."""

    return [
        {
            "index": index,
            "x": round(float(point.x), 7),
            "y": round(float(point.y), 7),
            "z": round(float(point.z), 7),
        }
        for index, point in enumerate(face_landmarks)
    ]


def extract_blendshapes(blendshape_result) -> list[dict]:
    """Extrai as categorias de expressão facial."""

    if not blendshape_result:
        return []

    return [
        {
            "name": category.category_name,
            "score": round(float(category.score), 7),
            "index": category.index,
        }
        for category in blendshape_result
    ]


def extract_transformation_matrix(matrix_result):
    """Converte a matriz facial 4x4 em uma lista Python."""

    if matrix_result is None:
        return None

    matrix = np.asarray(matrix_result, dtype=np.float64)

    if matrix.shape != (4, 4):
        raise ValueError(
            "A matriz de transformação facial precisa ser 4x4."
        )

    return np.round(matrix, 7).tolist()