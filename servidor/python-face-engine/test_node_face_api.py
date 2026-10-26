
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

print(f"2. Enviando {len(image_bytes)} bytes à API Node.js...")

api_request = urllib.request.Request(
    "http://127.0.0.1:3000/api/face/analyze",
    data=image_bytes,
    headers={"Content-Type": "image/jpeg"},
    method="POST",
)

with urllib.request.urlopen(api_request, timeout=60) as response:
    result = json.loads(response.read())

print("\n3. Resultado da análise:")
print("Motor:", result.get("engine"))
print("Rostos:", result.get("faceCount"))
print("Pontos faciais:", len(result.get("landmarks", [])))
print("Categorias de expressão:", len(result.get("blendshapes", [])))
print("Matriz disponível:", bool(result.get("transformationMatrix")))
print("Tempo de análise (ms):", result.get("processingMs"))

print("\n4. Perfil facial calculado pela API Node.js:")
profile = result.get("profile")

if not isinstance(profile, dict):
    raise RuntimeError(
        "O perfil facial não foi encontrado. "
        "Confira a integração em src/routes/face.routes.ts."
    )

measurements = profile.get("measurements", {})
quality = profile.get("quality", {})

print("Versão do perfil:", profile.get("schemaVersion"))
print("Versão do modelo:", profile.get("modelVersion"))
print("Quantidade de medidas:", len(measurements))
print("Estado da qualidade:", quality.get("status"))

for name, measurement in measurements.items():
    if isinstance(measurement, dict):
        value = measurement.get("value")
        available = measurement.get("available")
        print(f"- {name}: {value} (disponível: {available})")

print("\nAvisos:")
for warning in quality.get("warnings", []):
    print(f"- {warning}")

if len(measurements) != 10:
    raise RuntimeError(
        f"Esperadas 10 medidas; recebidas {len(measurements)}."
    )

print("\nSUCESSO: a API retornou o perfil facial com 10 medidas.")