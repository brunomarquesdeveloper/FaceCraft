
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Literal, TypedDict

import mediapipe as mp


# ---------------------------------------------------------------------
# IMAGEM
# ---------------------------------------------------------------------

@dataclass(frozen=True, slots=True)
class ImageData:
    """Imagem validada e preparada para o MediaPipe."""

    image: mp.Image
    width: int
    height: int


# ---------------------------------------------------------------------
# LANDMARKS
# ---------------------------------------------------------------------

class FaceLandmark(TypedDict):
    """Ponto facial em coordenadas normalizadas."""

    index: int
    x: float
    y: float
    z: float


# ---------------------------------------------------------------------
# BLENDSHAPES
# ---------------------------------------------------------------------

class FaceBlendshape(TypedDict):
    """Categoria de expressão facial."""

    name: str
    score: float
    index: int


# ---------------------------------------------------------------------
# GEOMETRIA FACIAL
# ---------------------------------------------------------------------

class FaceProfile(TypedDict):
    """Perfil facial independente das regras dos jogos."""

    version: str
    landmark_count: int
    geometry: dict[str, Any]


# ---------------------------------------------------------------------
# MATRIZ DE TRANSFORMAÇÃO
# ---------------------------------------------------------------------

TransformationMatrix = list[list[float]]


# ---------------------------------------------------------------------
# RESPOSTA DA ANÁLISE
# ---------------------------------------------------------------------

class FaceAnalysisResponse(TypedDict):
    """Estrutura principal retornada pela análise facial."""

    status: Literal["success"]
    engine: dict[str, str]
    face_count: int
    image: dict[str, Any]
    landmarks: dict[str, Any]
    blendshapes: dict[str, Any]
    geometry: dict[str, Any]
    transformation_matrix: TransformationMatrix | None
    processing_time_ms: float
