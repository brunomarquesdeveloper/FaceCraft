from fastapi import APIRouter, HTTPException

from app.schemas.face import AnalyzeFaceUrlRequest

from app.services.face.analyzer import (
    FaceAnalysisError,
    analyze_face_from_url,
)
from app.services.face.image_loader import ImageLoaderError
from app.services.face.landmarker import LandmarkerError
from app.services.face.profile_builder import FaceProfileError

from app.services.mapper.result_builder import build_mapping_result
from app.services.mapper.catalog_reader import CatalogReaderError


router = APIRouter(
    prefix="/api/face",
    tags=["Face Analysis"],
)


@router.post("/analyze-url")
def analyze_url(request: AnalyzeFaceUrlRequest):
    try:
        face_analysis = analyze_face_from_url(
            str(request.image_url)
        )

        result = build_mapping_result(
            slug=request.game_slug,
            face_analysis=face_analysis,
        )

        return result

    except CatalogReaderError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error),
        ) from error

    except (
        FaceAnalysisError,
        ImageLoaderError,
        FaceProfileError,
    ) as error:
        raise HTTPException(
            status_code=422,
            detail=str(error),
        ) from error

    except LandmarkerError as error:
        raise HTTPException(
            status_code=503,
            detail="O motor de análise facial não está disponível.",
        ) from error