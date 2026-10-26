import json
import time
import urllib.request
from pathlib import Path

import mediapipe as mp
from PIL import Image
from io import BytesIO

IMAGE_URL = (
    "https://img.magnific.com/fotos-gratis/"
    "retrato-de-homem-branco-isolado_53876-40306.jpg"
    "?semt=ais_hybrid&w=740&q=80"
)

ROOT = Path(__file__).resolve().parent.parent
MODEL_PATH = ROOT / "models" / "face_landmarker.task"
MAX_IMAGE_BYTES = 10 * 1024 * 1024


def main():
    if not MODEL_PATH.is_file():
        raise FileNotFoundError(f"Modelo não encontrado: {MODEL_PATH}")

    print("1. Baixando imagem de teste...")
    request = urllib.request.Request(
        IMAGE_URL,
        headers={"User-Agent": "FaceCraft/1.0"},
    )

    with urllib.request.urlopen(request, timeout=20) as response:
        content_type = response.headers.get("Content-Type", "")
        if not content_type.lower().startswith("image/"):
            raise ValueError(f"Resposta não é imagem: {content_type}")

        data = response.read(MAX_IMAGE_BYTES + 1)

    if not data or len(data) > MAX_IMAGE_BYTES:
        raise ValueError("Imagem vazia ou acima do limite de 10 MB")

    print(f"Imagem recebida: {len(data)} bytes")

    with Image.open(BytesIO(data)) as source:
        image = source.convert("RGB")
        print(f"Dimensões: {image.width}x{image.height}")
        image_data = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=__import__("numpy").array(image),
        )

    print("2. Carregando modelo Face Landmarker...")
    options = mp.tasks.vision.FaceLandmarkerOptions(
        base_options=mp.tasks.BaseOptions(
            model_asset_path=str(MODEL_PATH)
        ),
        running_mode=mp.tasks.vision.RunningMode.IMAGE,
        num_faces=1,
        output_face_blendshapes=True,
        output_facial_transformation_matrixes=True,
    )

    print("3. Analisando rosto...")
    start = time.perf_counter()

    with mp.tasks.vision.FaceLandmarker.create_from_options(options) as landmarker:
        result = landmarker.detect(image_data)

    elapsed_ms = round((time.perf_counter() - start) * 1000, 2)
    face_count = len(result.face_landmarks)

    report = {
        "engine": "MediaPipe Face Landmarker",
        "version": mp.__version__,
        "facesDetected": face_count,
        "processingMs": elapsed_ms,
        "model": MODEL_PATH.name,
    }

    if face_count:
        landmarks = result.face_landmarks[0]
        report["landmarkCount"] = len(landmarks)
        report["blendshapeCount"] = (
            len(result.face_blendshapes[0])
            if result.face_blendshapes
            else 0
        )
        report["transformationMatrixAvailable"] = bool(
            result.facial_transformation_matrixes
        )
        report["sampleLandmarks"] = [
            {"x": round(p.x, 5), "y": round(p.y, 5), "z": round(p.z, 5)}
            for p in landmarks[:3]
        ]

    print("4. Resultado:")
    print(json.dumps(report, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
