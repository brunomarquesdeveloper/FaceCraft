
from typing import Any

from app.services.mapper.catalog_reader import read_game_catalog
from app.services.mapper.feature_mapper import map_all_features


def build_mapping_result(
    slug: str,
    face_analysis: dict[str, Any],
) -> dict[str, Any]:

    if not isinstance(face_analysis, dict):
        raise ValueError("A análise facial precisa ser um objeto.")

    catalog = read_game_catalog(slug)

    features = map_all_features(
        profile=face_analysis,
        features=catalog["features"],
        mapping_policy=catalog["mapping_policy"],
    )

    customization = []

    for feature in features:
        customization.append({
            "feature_id": feature.get("feature_id"),
            "label": feature.get("feature_name"),
            "value": feature.get("value"),
            "status": feature.get("status"),
        })

    return {
        "game": slug,
        "customization": customization,
    }
