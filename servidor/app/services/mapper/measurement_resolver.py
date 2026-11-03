
from typing import Any


def _get_nested_value(data: Any, path: str) -> Any:
    """Busca um valor usando um caminho separado por pontos."""

    current = data

    for key in path.split("."):
        if not isinstance(current, dict):
            return None

        if key not in current:
            return None

        current = current[key]

    return current


def _get_search_roots(profile: dict[str, Any]) -> list[dict[str, Any]]:
    """Identifica as possíveis raízes do perfil facial."""

    roots = []

    face_profile = profile.get("face_profile")

    if isinstance(face_profile, dict):
        geometry = face_profile.get("geometry")

        if isinstance(geometry, dict):
            roots.append(geometry)

        roots.append(face_profile)

    geometry = profile.get("geometry")

    if isinstance(geometry, dict):
        roots.append(geometry)

    roots.append(profile)

    return roots


def resolve_measurement(
    profile: dict[str, Any],
    measurement_path: str,
) -> dict[str, Any]:
    """Localiza uma medição sem inventar ou alterar seu valor."""

    if not isinstance(measurement_path, str) or not measurement_path:
        return {
            "path": measurement_path,
            "available": False,
            "value": None,
        }

    roots = _get_search_roots(profile)

    paths_to_try = [measurement_path]

    if measurement_path.startswith("geometry."):
        paths_to_try.append(measurement_path[len("geometry."):])

    for root in roots:
        for path in paths_to_try:
            value = _get_nested_value(root, path)

            if value is not None:
                return {
                    "path": measurement_path,
                    "available": True,
                    "value": value,
                }

    return {
        "path": measurement_path,
        "available": False,
        "value": None,
    }


def resolve_feature_measurements(
    profile: dict[str, Any],
    feature: dict[str, Any],
) -> list[dict[str, Any]]:
    """Resolve todas as medições exigidas por uma característica."""

    source_measurements = feature.get("source_measurements", [])

    if not isinstance(source_measurements, list):
        return []

    results = []

    for measurement in source_measurements:
        if isinstance(measurement, str):
            path = measurement
        elif isinstance(measurement, dict):
            path = measurement.get("path") or measurement.get("id")
        else:
            continue

        if not isinstance(path, str) or not path:
            continue

        results.append(
            resolve_measurement(profile, path)
        )

    return results
