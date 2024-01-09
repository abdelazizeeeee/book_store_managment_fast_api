from pydantic import BaseModel



class Book(BaseModel):
    title : str
    author : str
    genre : str
    publication_date : str
    price : float


class Reviews(BaseModel):
    rating : int
    comment : str