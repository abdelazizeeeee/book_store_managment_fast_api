from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Depends, HTTPException, status
from .config.database import books, database, review
# from src.config.settings import settings
# from src.config.database import startDB

# from src.routes import auth, user
from .models.books import Book
from .models.reviews import Reviews


app = FastAPI()

# app.include_router(auth.router, tags=['Auth'], prefix='/api/auth')
# app.include_router(user.router, tags=['Users'], prefix='/api/users')


# Aziz
# Endpoint to get book details
@app.get("/api/books/{book_id}")
async def get_book_details(book_id: int):
    query = books.select().where(books.c.id == book_id)
    book = await database.fetch_one(query)

    if book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")

    return book


#  update book
@app.put("/api/books/{book_id}", status_code=status.HTTP_202_ACCEPTED)
async def update_book(book_id: int, updated_book: Book):
    query = books.update().where(books.c.id == book_id).values(updated_book.dict())

    # Execute the update query
    await database.execute(query)

    return {"message": "Book deleted successfully"}


# Endpoint to delete a book by ID
@app.delete("/api/books/{book_id}")
async def Delete_book(book_id: int):
    query = books.delete().where(books.c.id == book_id)
    await database.execute(query)
    return status.HTTP_204_NO_CONTENT, {"message": "Book updated successfully"}


# ADD NEW BOOK
@app.post("/api/books", status_code=status.HTTP_201_CREATED)
async def create_new_book(book: Book):
    query = books.insert().values(book.dict())

    last_record_id = await database.execute(query)

    return {"message": "Book created successfully", "book_id": last_record_id}

# Endpoint to get all books


@app.get("/api/books", response_model=list[Book])
async def get_all_books():
    query = books.select()
    all_books = await database.fetch_all(query)
    return all_books

# Souhaieb

# Get all review of a book


@app.get("/api/books/{book_id}/reviews", response_model=list[Reviews])
async def get_book_reviews(book_id: int):
    print(book_id)
    query = review.select().where(review.c.book_id == book_id)
    r = await database.fetch_all(query)
    print(r)

    if r is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")

    return r

# Create new review


@app.post("/api/books/{book_id}/reviews", status_code=status.HTTP_201_CREATED)
async def create_new_review(r: Reviews, book_id):
    r = r.dict()
    r["book_id"] = book_id
    query = review.insert().values(r)
    last_record_id = await database.execute(query)

    return {"message": "Review Added", "Review_id": last_record_id}
