from fastapi import FastAPI, Path, Query, Body
from pydantic import BaseModel

app = FastAPI()

# 📘 Step 1: Book Model
class Book(BaseModel):
    title: str
    author: str
    price: float
    summary: str | None = None

# 🔹 Step 2: Get book by ID (Path Parameter)
@app.get("/books/{book_id}")
async def get_book(
    book_id: int = Path(..., title="Book ID", description="ID must be 1 or greater", ge=1)
):
    return {"book_id": book_id, "message": "Book fetched successfully"}

# 🔹 Step 3: Search books (Query Parameters)
@app.get("/books/")
async def search_books(
    keyword: str | None = Query(None, min_length=3, max_length=50),
    limit: int = Query(10, le=100),
    skip: int = Query(0, ge=0)
):
    return {"keyword": keyword, "limit": limit, "skip": skip, "message": "Books search results"}

# 🔹 Step 4: Add or update a book (Request Body + Validation)
@app.put("/books/{book_id}")
async def update_book(
    book_id: int = Path(..., ge=1, title="Book ID"),
    q: str | None = Query(None, min_length=3),
    book: Book = Body(...)
):
    result = {"book_id": book_id, "message": "Book updated"}
    if q:
        result["query"] = q
    result["book_data"] = book.model_dump()
    return result
