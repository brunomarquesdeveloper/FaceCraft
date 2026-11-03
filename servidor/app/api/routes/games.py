from fastapi import APIRouter, HTTPException

from app.services.games.catalog import (
    get_all_games,
    get_game_config,
)

router = APIRouter(
    prefix="/api/games",
    tags=["Games"],
)


@router.get("/")
def list_games():
    games = get_all_games()

    return {
        "total": len(games),
        "games": games,
    }


@router.get("/{slug}/config")
def game_config(slug: str):
    config = get_game_config(slug)

    if config is None:
        raise HTTPException(
            status_code=404,
            detail="Configuração do jogo não encontrada.",
        )

    return config