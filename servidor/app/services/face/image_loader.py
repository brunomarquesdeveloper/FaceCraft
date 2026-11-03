from __future__ import annotations

from io import BytesIO
from urllib.parse import urlparse
import ipaddress
import socket
import warnings

import httpx
import numpy as np
from PIL import Image, UnidentifiedImageError
import mediapipe as mp

from app.services.face.schemas import ImageData


MAX_IMAGE_BYTES = 10 * 1024 * 1024
MAX_IMAGE_PIXELS = 20_000_000

ALLOWED_CONTENT_TYPES = {
    "image/jpeg",
    "image/png",
    "image/webp",
}


class ImageLoaderError(Exception):
    """Erro durante o download ou a validação da imagem."""


def validate_public_url(url: str) -> str:
    """Valida uma URL pública antes de iniciar o download."""

    try:
        parsed = urlparse(url)

        if parsed.scheme not in {"http", "https"}:
            raise ImageLoaderError(
                "A URL precisa utilizar HTTP ou HTTPS."
            )

        if not parsed.hostname:
            raise ImageLoaderError("URL inválida.")

        if parsed.username or parsed.password:
            raise ImageLoaderError(
                "URLs com credenciais não são permitidas."
            )

        hostname = parsed.hostname.lower()

        if hostname.endswith("."):
            hostname = hostname[:-1]

        if hostname in {"localhost", "localhost.localdomain"}:
            raise ImageLoaderError(
                "Endereços locais não são permitidos."
            )

        try:
            addresses = [
                ipaddress.ip_address(hostname)
            ]
        except ValueError:
            try:
                addresses = [
                    ipaddress.ip_address(item[4][0])
                    for item in socket.getaddrinfo(
                        hostname,
                        parsed.port or (
                            443 if parsed.scheme == "https" else 80
                        ),
                        type=socket.SOCK_STREAM,
                    )
                ]
            except socket.gaierror as exc:
                raise ImageLoaderError(
                    "Não foi possível resolver o endereço da imagem."
                ) from exc

        if not addresses or any(
            not address.is_global for address in addresses
        ):
            raise ImageLoaderError(
                "A URL aponta para um endereço não público."
            )

        return url

    except ImageLoaderError:
        raise

    except Exception as exc:
        raise ImageLoaderError("URL inválida.") from exc


def download_image(url: str) -> ImageData:
    """Baixa, valida e prepara uma imagem RGB para o MediaPipe."""

    validate_public_url(url)

    try:
        with httpx.Client(
            timeout=15.0,
            follow_redirects=False,
            headers={
                "User-Agent": "FaceCraft/1.0",
                "Accept": "image/jpeg,image/png,image/webp",
            },
        ) as client:

            with client.stream("GET", url) as response:
                if response.is_redirect:
                    raise ImageLoaderError(
                        "Redirecionamentos não são permitidos."
                    )

                response.raise_for_status()

                content_type = (
                    response.headers.get("content-type", "")
                    .split(";")[0]
                    .strip()
                    .lower()
                )

                if content_type not in ALLOWED_CONTENT_TYPES:
                    raise ImageLoaderError(
                        "Formato não permitido. Utilize JPEG, PNG ou WebP."
                    )

                content_length = response.headers.get("content-length")

                if content_length:
                    try:
                        if int(content_length) > MAX_IMAGE_BYTES:
                            raise ImageLoaderError(
                                "A imagem ultrapassa o limite de 10 MB."
                            )
                    except ValueError as exc:
                        raise ImageLoaderError(
                            "Tamanho de imagem inválido."
                        ) from exc

                image_data = bytearray()

                for chunk in response.iter_bytes():
                    image_data.extend(chunk)

                    if len(image_data) > MAX_IMAGE_BYTES:
                        raise ImageLoaderError(
                            "A imagem ultrapassa o limite de 10 MB."
                        )

        with warnings.catch_warnings():
            warnings.simplefilter(
                "error",
                Image.DecompressionBombWarning,
            )

            image = Image.open(BytesIO(image_data))

            if image.format not in {"JPEG", "PNG", "WEBP"}:
                raise ImageLoaderError(
                    "O conteúdo recebido não é uma imagem permitida."
                )

            width, height = image.size

            if (
                width <= 0
                or height <= 0
                or width * height > MAX_IMAGE_PIXELS
            ):
                raise ImageLoaderError(
                    "A imagem possui dimensões inválidas ou excessivas."
                )

            image.load()
            rgb_image = image.convert("RGB")

        image_array = np.asarray(rgb_image, dtype=np.uint8)

        mp_image = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=image_array,
        )

        return ImageData(
            image=mp_image,
            width=width,
            height=height,
        )

    except ImageLoaderError:
        raise

    except httpx.HTTPStatusError as exc:
        raise ImageLoaderError(
            f"Falha no download: HTTP {exc.response.status_code}."
        ) from exc

    except httpx.RequestError as exc:
        raise ImageLoaderError(
            "Falha de conexão ao baixar a imagem."
        ) from exc

    except (
        UnidentifiedImageError,
        Image.DecompressionBombError,
        Image.DecompressionBombWarning,
    ) as exc:
        raise ImageLoaderError(
            "A imagem está corrompida ou possui dimensões inseguras."
        ) from exc

    except Exception as exc:
        raise ImageLoaderError(
            "Não foi possível processar a imagem."
        ) from exc