import os
from pydantic_settings import BaseSettings
DATABASE_URL = "sqlite:///./test.db"


class Settings(BaseSettings):
    DATABASE_URL: str = os.getenv("DATABASE_URL", "default_database_url")
    # Other variables with default values

    # MONGO_INITDB_DATABASE: str = os.environ["MONGO_INITDB_DATABASE"]

    # JWT_PUBLIC_KEY: str = os.environ["JWT_PUBLIC_KEY"]
    # JWT_PRIVATE_KEY: str = os.environ["JWT_PRIVATE_KEY"]
    # REFRESH_TOKEN_EXPIRES_IN: int = os.environ["REFRESH_TOKEN_EXPIRES_IN"]
    # ACCESS_TOKEN_EXPIRES_IN: int = os.environ["ACCESS_TOKEN_EXPIRES_IN"]
    # JWT_ALGORITHM: str = os.environ["JWT_ALGORITHM"]

    # CLIENT_ORIGIN: str = os.environ["CLIENT_ORIGIN"]
        
settings = Settings()