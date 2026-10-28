
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.health import router as health_router

app = FastAPI(
    title="FaceCraft API",
    description="API de análise facial e personalização de personagens.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)


@app.get("/api/health", tags=["Health"])
def health():
    return {
        "status": "ok",
        "service": "FaceCraft API",
        "engine": "MediaPipe",
    }
