
from __future__ import annotations

from time import perf_counter

from app.services.face.image_loader import (
    download_image,
    ImageLoaderError,
)
from app.services.face.landmarker import (
    get_landmarker,
    LandmarkerError,
)
from app.services.face.extractors import (
    extract_landmarks,
    extract_blendshapes,
    extract_transformation_matrix,
)
from app.services.face.profile_builder import (
    build_face_profile,
    FaceProfileError,
)


class FaceAnalysisError(Exception):
    """Erro controlado durante a análise facial."""


def analyze_face_from_url(url: str) -> dict:
    """
    Executa a análise facial completa do FaceCraft.

    Retorna:
    - landmarks;
    - blendshapes;
    - geometria facial;
    - matriz de transformação;
    - dimensões da imagem;
    - tempo de processamento.
    """

    start_time = perf_counter()

    try:
        # 1. Baixar e validar imagem
        image_data = download_image(url)

        # 2. Carregar motor facial
        landmarker = get_landmarker()

        # 3. Executar detecção
        result = landmarker.detect(image_data.image)

        if not result.face_landmarks:
            raise FaceAnalysisError(
                "Nenhum rosto foi encontrado na imagem."
            )

        if len(result.face_landmarks) != 1:
            raise FaceAnalysisError(
                "A imagem precisa conter somente um rosto."
            )

        # 4. Extrair landmarks
        face_landmarks = result.face_landmarks[0]

        landmarks = extract_landmarks(face_landmarks)

        # 5. Extrair blendshapes
        blendshapes = []

        if result.face_blendshapes:
            blendshapes = extract_blendshapes(
                result.face_blendshapes[0]
            )

        # 6. Extrair matriz de transformação
        transformation_matrix = None

        if result.facial_transformation_matrixes:
            transformation_matrix = (
                extract_transformation_matrix(
                    result.facial_transformation_matrixes[0]
                )
            )

        # 7. Construir perfil facial
        profile = build_face_profile(
            landmarks=landmarks,
            image_width=image_data.width,
            image_height=image_data.height,
        )

        # 8. Calcular tempo
        processing_time = (
            perf_counter() - start_time
        ) * 1000

        # 9. Retornar resultado completo
        return {
            "status": "success",

            "engine": {
                "name": "mediapipe-face-landmarker",
                "version": "1.1.1",
            },

            "face_count": len(result.face_landmarks),

            "image": {
                "width": image_data.width,
                "height": image_data.height,
                "format": "RGB",
            },

            "landmarks": {
                "count": len(landmarks),
                "points": landmarks,
            },

            "blendshapes": {
                "count": len(blendshapes),
                "categories": blendshapes,
            },

            "geometry": profile["geometry"],

            "face_profile": profile,

            "transformation_matrix": transformation_matrix,

            "processing_time_ms": round(
                processing_time,
                2,
            ),
        }

    except (
        FaceAnalysisError,
        ImageLoaderError,
        LandmarkerError,
        FaceProfileError,
    ):
        raise

    except Exception as exc:
        raise FaceAnalysisError(
            "Ocorreu um erro inesperado durante a análise facial."
        ) from exc
