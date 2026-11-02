
from __future__ import annotations

from functools import lru_cache
from io import BytesIO
from pathlib import Path
from time import perf_counter
from urllib.parse import urlparse
import ipaddress
import socket
import warnings

import httpx
import mediapipe as mp
import numpy as np

from PIL import Image, UnidentifiedImageError

from mediapipe.tasks import python
from mediapipe.tasks.python import vision

from app.services.face_geometry import (
    calculate_face_geometry,
    FaceGeometryError,
)


# ---------------------------------------------------------------------
# CONFIGURAÇÕES
# ---------------------------------------------------------------------

MODEL_PATH = (
    Path(__file__).resolve().parents[2]
    / "models"
    / "face_landmarker.task"
)

MAX_IMAGE_BYTES = 10 * 1024 * 1024
MAX_IMAGE_PIXELS = 20_000_000

ALLOWED_CONTENT_TYPES = {
    "image/jpeg",
    "image/png",
    "image/webp",
}


# ---------------------------------------------------------------------
# ERROS
# ---------------------------------------------------------------------

class FaceAnalysisError(Exception):
    """Erro controlado durante a análise facial."""


# ---------------------------------------------------------------------
# VALIDAÇÃO DE URL
# ---------------------------------------------------------------------

def validate_public_url(url: str) -> str:
    """
    Valida URLs públicas antes de baixar uma imagem.

    Esta validação é uma proteção inicial contra SSRF.
    Para produção, também será necessário controlar a resolução DNS
    e o destino efetivo da conexão HTTP.
    """

    try:
        parsed = urlparse(url)

        if parsed.scheme not in {"http", "https"}:
            raise FaceAnalysisError(
                "A URL precisa utilizar HTTP ou HTTPS."
            )

        if not parsed.hostname:
            raise FaceAnalysisError(
                "A URL informada não possui um endereço válido."
            )

        if parsed.username or parsed.password:
            raise FaceAnalysisError(
                "URLs com credenciais não são permitidas."
            )

        hostname = parsed.hostname.lower()

        if hostname in {"localhost", "localhost.localdomain"}:
            raise FaceAnalysisError(
                "Endereços locais não são permitidos."
            )

        try:
            ip = ipaddress.ip_address(hostname)

            if not ip.is_global:
                raise FaceAnalysisError(
                    "Endereços IP privados não são permitidos."
                )

        except ValueError:
            try:
                addresses = socket.getaddrinfo(
                    hostname,
                    parsed.port or (443 if parsed.scheme == "https" else 80),
                    type=socket.SOCK_STREAM,
                )

                if not addresses:
                    raise FaceAnalysisError(
                        "Não foi possível localizar o endereço da imagem."
                    )

                for address in addresses:
                    resolved_ip = ipaddress.ip_address(
                        address[4][0]
                    )

                    if not resolved_ip.is_global:
                        raise FaceAnalysisError(
                            "A URL aponta para um endereço não público."
                        )

            except socket.gaierror as exc:
                raise FaceAnalysisError(
                    "Não foi possível resolver o endereço da imagem."
                ) from exc

        return url

    except FaceAnalysisError:
        raise

    except Exception as exc:
        raise FaceAnalysisError(
            "URL de imagem inválida."
        ) from exc


# ---------------------------------------------------------------------
# DOWNLOAD E VALIDAÇÃO DA IMAGEM
# ---------------------------------------------------------------------

def download_image(url: str) -> tuple[Image.Image, int, int]:
    """
    Baixa e valida uma imagem pública.

    Limites:
    - 10 MB por imagem;
    - 20 milhões de pixels;
    - JPEG, PNG e WebP;
    - sem redirecionamentos automáticos.
    """

    validate_public_url(url)

    headers = {
        "User-Agent": "FaceCraft/1.0",
        "Accept": "image/jpeg,image/png,image/webp",
    }

    try:
        with httpx.Client(
            timeout=15.0,
            follow_redirects=False,
            headers=headers,
        ) as client:

            with client.stream("GET", url) as response:
                response.raise_for_status()

                if response.is_redirect:
                    raise FaceAnalysisError(
                        "Redirecionamentos de imagem não são permitidos."
                    )

                content_type = (
                    response.headers
                    .get("content-type", "")
                    .split(";")[0]
                    .strip()
                    .lower()
                )

                if content_type not in ALLOWED_CONTENT_TYPES:
                    raise FaceAnalysisError(
                        "Formato de imagem não permitido. "
                        "Utilize JPEG, PNG ou WebP."
                    )

                content_length = response.headers.get(
                    "content-length"
                )

                if content_length:
                    try:
                        if int(content_length) > MAX_IMAGE_BYTES:
                            raise FaceAnalysisError(
                                "A imagem ultrapassa o limite de 10 MB."
                            )
                    except ValueError:
                        raise FaceAnalysisError(
                            "Tamanho de imagem inválido."
                        )

                image_data = bytearray()

                for chunk in response.iter_bytes():
                    image_data.extend(chunk)

                    if len(image_data) > MAX_IMAGE_BYTES:
                        raise FaceAnalysisError(
                            "A imagem ultrapassa o limite de 10 MB."
                        )

        with warnings.catch_warnings():
            warnings.simplefilter(
                "error",
                Image.DecompressionBombWarning,
            )

            image = Image.open(BytesIO(image_data))

            if image.format not in {"JPEG", "PNG", "WEBP"}:
                raise FaceAnalysisError(
                    "O conteúdo recebido não é uma imagem permitida."
                )

            width, height = image.size

            if width <= 0 or height <= 0:
                raise FaceAnalysisError(
                    "A imagem possui dimensões inválidas."
                )

            if width * height > MAX_IMAGE_PIXELS:
                raise FaceAnalysisError(
                    "A imagem ultrapassa o limite de 20 milhões de pixels."
                )

            image.load()
            image = image.convert("RGB")

        return image, width, height

    except FaceAnalysisError:
        raise

    except httpx.HTTPStatusError as exc:
        raise FaceAnalysisError(
            f"Não foi possível baixar a imagem. "
            f"Servidor respondeu com HTTP {exc.response.status_code}."
        ) from exc

    except httpx.RequestError as exc:
        raise FaceAnalysisError(
            "Falha de conexão ao baixar a imagem."
        ) from exc

    except (
        UnidentifiedImageError,
        Image.DecompressionBombError,
        Image.DecompressionBombWarning,
    ) as exc:
        raise FaceAnalysisError(
            "A imagem está corrompida ou possui dimensões inseguras."
        ) from exc

    except FaceAnalysisError:
        raise

    except Exception as exc:
        raise FaceAnalysisError(
            "Não foi possível processar a imagem recebida."
        ) from exc


# ---------------------------------------------------------------------
# CARREGAMENTO DO MODELO MEDIAPIPE
# ---------------------------------------------------------------------

@lru_cache(maxsize=1)
def get_landmarker():
    """
    Carrega o modelo uma única vez e reutiliza o motor nas análises.
    """

    if not MODEL_PATH.exists():
        raise FaceAnalysisError(
            f"Modelo facial não encontrado: {MODEL_PATH}"
        )

    try:
        base_options = python.BaseOptions(
            model_asset_path=str(MODEL_PATH)
        )

        options = vision.FaceLandmarkerOptions(
            base_options=base_options,
            running_mode=vision.RunningMode.IMAGE,
            num_faces=1,
            min_face_detection_confidence=0.5,
            min_face_presence_confidence=0.5,
            min_tracking_confidence=0.5,
            output_face_blendshapes=False,
            output_facial_transformation_matrixes=True,
        )

        return vision.FaceLandmarker.create_from_options(options)

    except Exception as exc:
        raise FaceAnalysisError(
            "Não foi possível inicializar o MediaPipe Face Landmarker."
        ) from exc


# ---------------------------------------------------------------------
# EXTRAÇÃO DOS LANDMARKS
# ---------------------------------------------------------------------

def extract_landmarks(face_landmarks) -> list[dict]:
    """
    Converte os landmarks do MediaPipe em dados serializáveis.
    """

    landmarks = []

    for index, point in enumerate(face_landmarks):

        landmarks.append({
            "index": index,
            "x": round(float(point.x), 7),
            "y": round(float(point.y), 7),
            "z": round(float(point.z), 7),
        })

    return landmarks


# ---------------------------------------------------------------------
# EXTRAÇÃO DOS BLENDSHAPES
# ---------------------------------------------------------------------

def extract_blendshapes(blendshape_result) -> list[dict]:
    """
    Extrai as categorias de expressão facial do MediaPipe.
    """

    if not blendshape_result:
        return []

    categories = []

    for category in blendshape_result:

        categories.append({
            "name": category.category_name,
            "score": round(float(category.score), 7),
            "index": category.index,
        })

    return categories


# ---------------------------------------------------------------------
# EXTRAÇÃO DA MATRIZ DE TRANSFORMAÇÃO
# ---------------------------------------------------------------------

def extract_transformation_matrix(matrix_result):
    """
    Converte a matriz facial 4x4 em uma lista Python.
    """

    if matrix_result is None:
        return None

    matrix = np.asarray(matrix_result, dtype=np.float64)

    return np.round(matrix, 7).tolist()


# ---------------------------------------------------------------------
# ANÁLISE FACIAL COMPLETA
# ---------------------------------------------------------------------

def analyze_face_from_url(url: str) -> dict:
    """
    Executa a análise facial a partir de uma URL pública.

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
        # 1. Baixar e validar a imagem
        image, image_width, image_height = download_image(url)

        # 2. Preparar imagem para o MediaPipe
        image_array = np.asarray(image, dtype=np.uint8)

        mp_image = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=image_array,
        )

        # 3. Carregar o motor facial
        landmarker = get_landmarker()

        # 4. Executar detecção facial
        result = landmarker.detect(mp_image)

        if not result.face_landmarks:
            raise FaceAnalysisError(
                "Nenhum rosto foi encontrado na imagem."
            )

        if len(result.face_landmarks) != 1:
            raise FaceAnalysisError(
                "A imagem precisa conter somente um rosto."
            )

        # 5. Extrair os landmarks
        face_landmarks = result.face_landmarks[0]

        landmarks = extract_landmarks(face_landmarks)

        # 6. Extrair blendshapes
        blendshapes = []

        if result.face_blendshapes:
            blendshapes = extract_blendshapes(
                result.face_blendshapes[0]
            )

        # 7. Extrair matriz de transformação
        transformation_matrix = None

        if result.facial_transformation_matrixes:
            transformation_matrix = extract_transformation_matrix(
                result.facial_transformation_matrixes[0]
            )

        # 8. Calcular geometria facial
        try:
            geometry = calculate_face_geometry(
                landmarks=landmarks,
                image_width=image_width,
                image_height=image_height,
            )

        except FaceGeometryError:
            raise

        except Exception as exc:
            raise FaceAnalysisError(
                "Falha ao calcular a geometria facial."
            ) from exc

        # 9. Calcular tempo de processamento
        processing_time = (
            perf_counter() - start_time
        ) * 1000

        # 10. Retornar perfil facial
        return {
            "status": "success",
            "engine": {
                "name": "mediapipe-face-landmarker",
                "version": "1.1.1",
            },
            "face_count": len(result.face_landmarks),
            "image": {
                "width": image_width,
                "height": image_height,
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
            "geometry": geometry,
            "transformation_matrix": transformation_matrix,
            "processing_time_ms": round(
                processing_time,
                2,
            ),
        }

    except FaceAnalysisError:
        raise

    except Exception as exc:
        raise FaceAnalysisError(
            "Ocorreu um erro inesperado durante a análise facial."
        ) from exc
