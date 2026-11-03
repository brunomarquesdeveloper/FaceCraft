"""
Compatibilidade com o caminho antigo de importação.

A implementação foi dividida em app.services.face.geometry.
"""

from app.services.face.geometry import (
    calculate_face_geometry,
    FaceGeometryError,
)

__all__ = ["calculate_face_geometry", "FaceGeometryError"]
