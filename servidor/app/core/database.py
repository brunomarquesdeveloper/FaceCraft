import psycopg
from app.core.config import settings


def get_database_connection():
    database_url = settings.neon_database_url

    if not database_url:
        raise RuntimeError(
            "DATABASE_URL não configurada no arquivo .env."
        )

    return psycopg.connect(
        database_url,
        connect_timeout=10,
        sslmode="require",
    )