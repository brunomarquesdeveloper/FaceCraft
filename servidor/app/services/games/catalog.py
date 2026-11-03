import json

from pathlib import Path

GAMES_DIR = Path(__file__).resolve().parents[3] / "games"


def get_all_games():
    games = []

    for config_path in sorted(GAMES_DIR.glob("*.json")):
        try:
            with config_path.open("r", encoding="utf-8") as file:
                config = json.load(file)

            game = config.get("game", {})

            games.append({
                "id": game.get("id", config_path.stem),
                "slug": config_path.stem.split(".")[0],
                "name": game.get("name", config_path.stem),
                "config": config_path.name,
            })

        except (json.JSONDecodeError, OSError):
            continue

    return games


def get_game_config(slug: str):
    for config_path in GAMES_DIR.glob("*.json"):
        game_slug = config_path.stem.split(".")[0]

        if game_slug != slug:
            continue

        try:
            with config_path.open("r", encoding="utf-8") as file:
                return json.load(file)
        except (json.JSONDecodeError, OSError):
            return None

    return None