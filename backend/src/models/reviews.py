from pydantic import BaseModel


class Reviews(BaseModel):
    rating : int
    comment : str