from contextlib import asynccontextmanager
from io import BytesIO
from pathlib import Path
from time import perf_counter

import mediapipe as mp
import numpy as np
from fastapi import FastAPI, HTTPException, Request
from PIL import Image, UnidentifiedImageError

ROOT = Path(__file__).resolve().parent.parent
MODEL_PATH = ROOT / "models" / "face_landmarker.task"

MAX_IMAGE_BYTES = 10 * 1024 * 1024
MAX_IMAGE_PIXELS = 20_000_000


@asynccontextmanager
async def lifespan(app: FastAPI):
    if not MODEL_PATH.is_file():
        raise RuntimeError(f"Modelo não encontrado: {MODEL_PATH}")

    options = mp.tasks.vision.FaceLandmarkerOptions(
        base_options=mp.tasks.BaseOptions(
            model_asset_path=str(MODEL_PATH)
        ),
        running_mode=mp.tasks.vision.RunningMode.IMAGE,
        num_faces=1,
        output_face_blendshapes=True,
        output_facial_transformation_matrixes=True,
    )

    app.state.landmarker = (
        mp.tasks.vision.FaceLandmarker.create_from_options(options)
    )

    yield

    app.state.landmarker.close()


app = FastAPI(
    title="FaceCraft Face Engine",
    version="1.0.0",
    lifespan=lifespan,
)


@app.get("/health")
def health():
    return {
        "status": "ok",
        "engine": "MediaPipe Face Landmarker",
        "version": mp.__version__,
    }


@app.post("/analyze")
async def analyze(request: Request):
    content_type = request.headers.get("content-type", "").lower()

    if content_type not in {
        "image/jpeg",
        "image/png",
        "image/webp",
    }:
        raise HTTPException(
            status_code=415,
            detail="Envie uma imagem JPEG, PNG ou WebP.",
        )

    content_length = request.headers.get("content-length")

    if content_length:
        try:
            if int(content_length) > MAX_IMAGE_BYTES:
                raise HTTPException(
                    status_code=413,
                    detail="A imagem excede o limite de 10 MB.",
                )
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail="Content-Length inválido.",
            )

    data = await request.body()

    if not data or len(data) > MAX_IMAGE_BYTES:
        raise HTTPException(
            status_code=413 if data else 400,
            detail="Imagem vazia ou acima do limite de 10 MB.",
        )

    try:
        with Image.open(BytesIO(data)) as source:
            if source.width * source.height > MAX_IMAGE_PIXELS:
                raise HTTPException(
                    status_code=413,
                    detail="A resolução da imagem é muito alta.",
                )

            source.load()
            rgb = np.array(source.convert("RGB"))

    except HTTPException:
        raise
    except (UnidentifiedImageError, OSError, ValueError):
        raise HTTPException(
            status_code=400,
            detail="O arquivo não contém uma imagem válida.",
        )

    image = mp.Image(
        image_format=mp.ImageFormat.SRGB,
        data=rgb,
    )

    started = perf_counter()
    result = request.app.state.landmarker.detect(image)
    elapsed_ms = round((perf_counter() - started) * 1000, 2)

    if not result.face_landmarks:
        raise HTTPException(
            status_code=422,
            detail="Nenhum rosto foi detectado. Tente outra foto.",
        )

    landmarks = result.face_landmarks[0]

    blendshapes = []
    if result.face_blendshapes:
        blendshapes = [
            {
                "name": item.category_name,
                "score": item.score,
                "displayName": item.display_name,
            }
            for item in result.face_blendshapes[0]
        ]

    matrix = None
    if result.facial_transformation_matrixes:
        matrix_array = np.asarray(
            result.facial_transformation_matrixes[0]
        )
        matrix = {
            "rows": int(matrix_array.shape[0]),
            "columns": int(matrix_array.shape[1]),
            "data": matrix_array.tolist(),
        }

    return {
        "engine": "mediapipe-face-landmarker",
        "modelVersion": mp.__version__,
        "image": {
            "width": int(rgb.shape[1]),
            "height": int(rgb.shape[0]),
        },
        "processingMs": elapsed_ms,
        "faceCount": len(result.face_landmarks),
        "landmarks": [
            {
                "x": point.x,
                "y": point.y,
                "z": point.z,
            }
            for point in landmarks
        ],
        "blendshapes": blendshapes,
        "transformationMatrix": matrix,
    }