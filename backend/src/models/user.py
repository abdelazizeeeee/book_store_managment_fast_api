from datetime import datetime
from pydantic import BaseModel
from typing import Optional
from beanie import Document
from ...src import utils


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str or None = None


class Users(BaseModel):
    username: str
    email: str or None = None
    full_name: str or None = None
    hashed_password: str
    disabled: bool or None = None


class UserInDB(Users):
    hashed_password: str
