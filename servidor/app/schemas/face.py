from pydantic import AnyHttpUrl, BaseModel


class AnalyzeFaceUrlRequest(BaseModel):
    image_url: AnyHttpUrl