from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from mediapipe.tasks import python
from mediapipe.tasks.python import vision


MODEL_PATH = (
    Path(__file__).resolve().parents[3]
    / "models"
    / "face_landmarker.task"
)


class LandmarkerError(Exception):
    """Erro durante a inicialização do motor facial."""


@lru_cache(maxsize=1)
def get_landmarker():
    """Carrega o modelo uma única vez por processo."""

    if not MODEL_PATH.is_file():
        raise LandmarkerError(
            f"Modelo facial não encontrado: {MODEL_PATH}"
        )

    try:
        base_options = python.BaseOptions(
            model_asset_path=str(MODEL_PATH)
        )

        options = vision.FaceLandmarkerOptions(
            base_options=base_options,
            running_mode=vision.RunningMode.IMAGE,
            num_faces=2,
            min_face_detection_confidence=0.5,
            min_face_presence_confidence=0.5,
            min_tracking_confidence=0.5,
            output_face_blendshapes=True,
            output_facial_transformation_matrixes=True,
        )

        return vision.FaceLandmarker.create_from_options(options)

    except Exception as exc:
        raise LandmarkerError(
            "Não foi possível inicializar o MediaPipe."
        ) from exc