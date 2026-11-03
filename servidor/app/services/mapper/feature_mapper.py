
from typing import Any
from app.services.mapper.measurement_resolver import (
    resolve_feature_measurements,
)


def normalize_value(
    value: float,
    minimum: float,
    maximum: float,
) -> float:
    """Converte uma medida para a escala interna de -1 a 1."""

    if maximum <= minimum:
        raise ValueError("Intervalo de calibração inválido.")

    normalized = (
        2 * (value - minimum) / (maximum - minimum)
    ) - 1

    return round(max(-1.0, min(1.0, normalized)), 4)


def calculate_axis(
    axis: dict[str, Any],
    measurements: list[dict[str, Any]],
) -> float | None:
    """
    Calcula um eixo usando as referências declaradas no catálogo.

    Cada eixo deve possuir:
    calibration:
      measurement: caminho da métrica
      min: limite inferior
      max: limite superior
      inverted: inverte a direção, opcional
    """

    calibration = axis.get("calibration")

    if not isinstance(calibration, dict):
        return None

    path = calibration.get("measurement")
    minimum = calibration.get("min")
    maximum = calibration.get("max")

    if not isinstance(path, str):
        return None

    if not isinstance(minimum, (int, float)):
        return None

    if not isinstance(maximum, (int, float)):
        return None

    measurement = next(
        (
            item for item in measurements
            if item["path"] == path and item["available"]
        ),
        None,
    )

    if measurement is None:
        return None

    raw_value = measurement.get("value")

    if not isinstance(raw_value, (int, float)):
        return None

    result = normalize_value(
        float(raw_value),
        float(minimum),
        float(maximum),
    )

    if calibration.get("inverted", False):
        result = -result

    return result


def map_feature(
    profile: dict[str, Any],
    feature: dict[str, Any],
    mapping_policy: dict[str, Any] | None = None,
) -> dict[str, Any]:

    measurements = resolve_feature_measurements(
        profile=profile,
        feature=feature,
    )

    available = [
        item for item in measurements
        if item["available"]
    ]

    missing = [
        item for item in measurements
        if not item["available"]
    ]

    axes = feature.get("axes", [])
    if not isinstance(axes, list):
        axes = []

    values = {}
    calculated = 0

    for axis in axes:
        axis_id = axis.get("id")

        if not isinstance(axis_id, str):
            continue

        value = calculate_axis(axis, measurements)

        values[axis_id] = value

        if value is not None:
            calculated += 1

    if not available:
        status = "insufficient_data"

    elif calculated == 0:
        status = "needs_calibration"

    elif missing or calculated < len(axes):
        status = "partial_recommendation"

    else:
        status = "recommended"

    presets = feature.get("presets", [])

    if not isinstance(presets, list):
        presets = []

    return {
        "feature_id": feature.get("id"),
        "feature_name": feature.get("name") or feature.get("label"),
        "value": values if calculated else None,
        "status": status,
        "presets": presets,
        "measurements_summary": {
            "total": len(measurements),
            "available": len(available),
            "missing": len(missing),
        },
    }


def map_all_features(
    profile: dict[str, Any],
    features: list[dict[str, Any]],
    mapping_policy: dict[str, Any] | None = None,
) -> list[dict[str, Any]]:

    return [
        map_feature(
            profile=profile,
            feature=feature,
            mapping_policy=mapping_policy,
        )
        for feature in features
    ]
