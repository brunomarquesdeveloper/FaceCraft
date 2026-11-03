
from typing import Any

from app.services.games.catalog import get_game_config


class CatalogReaderError(Exception):
    """Erro ao carregar ou interpretar o catálogo do jogo."""


def load_game_catalog(slug: str) -> dict[str, Any]:
    """Carrega o catálogo de um jogo pelo slug."""

    config = get_game_config(slug)

    if config is None:
        raise CatalogReaderError(
            f"Catálogo não encontrado para o jogo: {slug}"
        )

    if not isinstance(config, dict):
        raise CatalogReaderError("O catálogo precisa ser um objeto JSON.")

    required_fields = ("schema_version", "game", "features")

    for field in required_fields:
        if field not in config:
            raise CatalogReaderError(
                f"Campo obrigatório ausente no catálogo: {field}"
            )

    if not isinstance(config["game"], dict):
        raise CatalogReaderError("A seção 'game' é inválida.")

    if not isinstance(config["features"], list):
        raise CatalogReaderError("A seção 'features' precisa ser uma lista.")

    return config


def get_catalog_features(catalog: dict[str, Any]) -> list[dict[str, Any]]:
    """Retorna as características configuradas no catálogo."""

    features = catalog.get("features", [])

    return [
        feature
        for feature in features
        if isinstance(feature, dict)
    ]


def get_manual_controls(catalog: dict[str, Any]) -> dict[str, Any]:
    """Retorna os controles que exigem intervenção manual."""

    controls = catalog.get("manual_controls", {})

    return controls if isinstance(controls, dict) else {}


def get_mapping_policy(catalog: dict[str, Any]) -> dict[str, Any]:
    """Retorna as regras de segurança do mapeamento."""

    policy = catalog.get("mapping_policy", {})

    return policy if isinstance(policy, dict) else {}


def read_game_catalog(slug: str) -> dict[str, Any]:
    """Retorna o catálogo organizado para o mapper."""

    catalog = load_game_catalog(slug)

    return {
        "schema_version": catalog.get("schema_version"),
        "game": catalog["game"],
        "features": get_catalog_features(catalog),
        "manual_controls": get_manual_controls(catalog),
        "mapping_policy": get_mapping_policy(catalog),
        "coordinate_system": catalog.get("coordinate_system", {}),
        "scope": catalog.get("scope", {}),
    }
