from pydantic import BaseModel, HttpUrl


class AnalyzeFaceUrlRequest(BaseModel):
    image_url: HttpUrl
    game_slug: str