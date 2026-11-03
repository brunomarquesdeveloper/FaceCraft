from pprint import pprint

from app.services.face.analyzer import analyze_face_from_url

image_url = input("URL da imagem de teste: ").strip()

result = analyze_face_from_url(image_url)

profile = result.get("face_profile", result)
geometry = profile.get("geometry", {})

print("\n===== MEDIDAS FACIAIS REAIS =====")

for feature in (
    "face",
    "eyes",
    "nose",
    "mouth",
    "jaw",
    "chin",
    "eyebrows",
):
    print(f"\n--- {feature.upper()} ---")
    pprint(geometry.get(feature, {}))