from fastapi import APIRouter, HTTPException
from app.core.database import get_database_connection

router = APIRouter(prefix="/api", tags=["Health"])


@router.get("/health/database")
def database_health():
    try:
        with get_database_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT current_database()")
                row = cursor.fetchone()

        return {
            "status": "ok",
            "database": row[0],
        }

    except Exception:
        raise HTTPException(
            status_code=503,
            detail="Não foi possível conectar ao banco de dados.",
        )