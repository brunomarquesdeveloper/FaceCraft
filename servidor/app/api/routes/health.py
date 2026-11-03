from fastapi import APIRouter

from app.services.games.catalog import get_all_games

router = APIRouter(
    prefix="/api",
    tags=["Health"],
)


@router.get("/health")
def health():
    games = get_all_games()

    return {
        "status": "ok",
        "service": "FaceCraft API",
        "engine": "MediaPipe",
        "games": {
            "status": "ok",
            "total": len(games),
            "available": [
                game["slug"] for game in games
            ],
        },
    }
