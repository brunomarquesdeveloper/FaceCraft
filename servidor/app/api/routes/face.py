from fastapi import APIRouter, HTTPException

from app.schemas.face import AnalyzeFaceUrlRequest
from app.services.face_analyzer import (
    FaceAnalysisError,
    analyze_face_from_url,
)

router = APIRouter(prefix="/api/face", tags=["Face Analysis"])


@router.post("/analyze-url")
def analyze_url(request: AnalyzeFaceUrlRequest):
    try:
        return analyze_face_from_url(str(request.image_url))

    except FaceAnalysisError as error:
        raise HTTPException(status_code=422, detail=str(error))

    except RuntimeError:
        raise HTTPException(
            status_code=503,
            detail="O motor de análise facial não está disponível.",
        )
