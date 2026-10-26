import json
import urllib.request

image_url = (
    "https://img.magnific.com/fotos-gratis/"
    "retrato-de-homem-branco-isolado_53876-40306.jpg"
    "?semt=ais_hybrid&w=740&q=80"
)

print("1. Baixando a imagem...")
request = urllib.request.Request(
    image_url,
    headers={"User-Agent": "FaceCraft/1.0"},
)

with urllib.request.urlopen(request, timeout=20) as response:
    image_bytes = response.read(10 * 1024 * 1024 + 1)
    content_type = response.headers.get("Content-Type", "")

if not content_type.lower().startswith("image/jpeg"):
    raise RuntimeError(f"Tipo de imagem inesperado: {content_type}")

if not image_bytes or len(image_bytes) > 10 * 1024 * 1024:
    raise RuntimeError("Imagem vazia ou acima de 10 MB")

print(f"2. Enviando {len(image_bytes)} bytes ao motor facial...")

api_request = urllib.request.Request(
    "http://127.0.0.1:3000/api/face/analyze",
    data=image_bytes,
    headers={"Content-Type": "image/jpeg"},
    method="POST",
)

with urllib.request.urlopen(api_request, timeout=60) as response:
    result = json.loads(response.read())

print("\n3. Resultado:")
print("Motor:", result.get("engine"))
print("Rostos:", result.get("faceCount"))
print("Pontos faciais:", len(result.get("landmarks", [])))
print("Categorias de expressão:", len(result.get("blendshapes", [])))
print("Matriz disponível:", bool(result.get("transformationMatrix")))
print("Tempo de análise (ms):", result.get("processingMs"))
