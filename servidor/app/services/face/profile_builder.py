from __future__ import annotations

from app.services.face_geometry import (
    calculate_face_geometry,
    FaceGeometryError,
)


class FaceProfileError(Exception):
    """Erro durante a construção do perfil facial."""


def build_face_profile(
    landmarks: list[dict],
    image_width: int,
    image_height: int,
) -> dict:
    """
    Constrói o perfil facial independente das regras dos jogos.
    """

    if not landmarks:
        raise FaceProfileError(
            "Não existem landmarks para construir o perfil."
        )

    if image_width <= 0 or image_height <= 0:
        raise FaceProfileError(
            "As dimensões da imagem são inválidas."
        )

    try:
        geometry = calculate_face_geometry(
            landmarks=landmarks,
            image_width=image_width,
            image_height=image_height,
        )

    except FaceGeometryError:
        raise

    except Exception as exc:
        raise FaceProfileError(
            "Falha ao calcular a geometria facial."
        ) from exc

    return {
        "version": "1.0",
        "landmark_count": len(landmarks),
        "geometry": geometry,
    }