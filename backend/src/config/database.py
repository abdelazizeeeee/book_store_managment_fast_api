from .settings import settings
# from ..models.user import User
import databases,sqlalchemy
# from motor.motor_asyncio import AsyncIOMotorClient
from models.books import Book
# from beanie import init_beanie


# Call this from within your event loop to get beanie setup.
# async def startDB():
#     # Create Motor client
#     client = AsyncIOMotorClient(settings.DATABASE_URL)

#     # Init beanie with the Product document class
#     await init_beanie(database=client.db_name, document_models=[User])


DATABASE_URL = "sqlite:///./test.db"
database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

books = sqlalchemy.Table(
    "books",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, index=True),
    sqlalchemy.Column("title", sqlalchemy.String),
    sqlalchemy.Column("author", sqlalchemy.String),
    sqlalchemy.Column("genre", sqlalchemy.String),
    sqlalchemy.Column("publication_date", sqlalchemy.String),
    sqlalchemy.Column("price", sqlalchemy.Integer),
)
engine = sqlalchemy.create_engine(DATABASE_URL)
metadata.create_all(bind=engine)

review = sqlalchemy.Table(
    "review",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, index=True),
    sqlalchemy.Column("comment", sqlalchemy.String),
    sqlalchemy.Column("rating", sqlalchemy.Integer),
)
metadata.drop_all(bind=engine)
metadata.create_all(bind=engine)
