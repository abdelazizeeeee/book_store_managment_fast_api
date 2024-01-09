from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Depends, HTTPException, status
from config.database import books,database
from src.config.settings import settings
from src.config.database import startDB

from src.routes import auth, user
from models.books import Book



app = FastAPI()

origins = [
    settings.CLIENT_ORIGIN,
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def start_dependencies():
    await startDB()
    # await startMinio()


app.include_router(auth.router, tags=['Auth'], prefix='/api/auth')
app.include_router(user.router, tags=['Users'], prefix='/api/users')


@app.get("/api/healthchecker")
def root():
    return {"message": "Welcome to FastAPI with MongoDB"}


# Endpoint to get book details
@app.get("/api/books/{book_id}")
async def Book_details(book:Book):
    return book



@app.put("/api/books/{book_id}")
async def Update_book(book: Book):
    return book, status.HTTP_202_ACCEPTED



@app.delete("/api/books/{book_id}")
async def Delete_book(book:Book):
    pass


@app.post("/api/books", status_code=status.HTTP_201_CREATED)
async def create_new_book(book: Book):
    query = books.insert().values(book.dict())

    last_record_id = await database.execute(query)

    return {"message": "Book created successfully", "book_id": last_record_id}