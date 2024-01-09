from pydantic import BaseModel


class Reviews(BaseModel):
    comment: str
    rating: int
