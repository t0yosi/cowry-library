from fastapi import APIRouter, HTTPException, Query, Body
from models import Book
from database import db
from bson import ObjectId
from typing import Optional, List
from datetime import datetime, timedelta
from pydantic import BaseModel
from models import BookFilter
from rabbitmq import notify_book_borrowed

router = APIRouter()


@router.get("/")
async def list_books():
    books = list(db.books.find({"is_borrowed": False}, {"_id": 0}))
    return {"books": books}


@router.get("/{book_id}")
async def get_book_by_id(book_id: str):
    # Check if the provided ID is a valid ObjectId format
    if not ObjectId.is_valid(book_id):
        raise HTTPException(status_code=400, detail="Invalid ID format")

    # Fetch the book from the database
    book = db.books.find_one({"_id": ObjectId(book_id)})

    # If the book is found, convert ObjectId to string and return the book
    if book:
        book["_id"] = str(book["_id"])  # Convert ObjectId to string
        return book

    # If no book is found, raise a 404 Not Found error
    raise HTTPException(status_code=404, detail="Book not found")


@router.get("/filter/")
async def filter_books(publisher: Optional[str] = None, category: Optional[str] = None):
    filters = {}
    if publisher:
        filters["publisher"] = publisher
    if category:
        filters["category"] = category

    # Print filters for debugging
    print(f"Filters applied: {filters}")

    # Query MongoDB with filters
    books = list(db.books.find(filters, {"_id": 0}))

    # Print results for debugging
    print(f"Books found: {books}")

    return {"books": books}

class BorrowRequest(BaseModel):
    days: int


@router.post("/{book_id}/borrow")
async def borrow_book(book_id: str, borrow_request: BorrowRequest):
    
    # Search for the book by UUID
    book = db.books.find_one({"uuid": book_id})
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    if book["is_borrowed"]:
        raise HTTPException(status_code=400, detail="Book is already borrowed")

    due_date = (datetime.utcnow() + timedelta(days=borrow_request.days)).date().isoformat()
    db.books.update_one(
        {"uuid": book_id}, {"$set": {"is_borrowed": True, "due_date": due_date}}
    )

    print(due_date)

    # Notify backend API about the borrowed book
    user_id = 1
    notify_book_borrowed({
        "book_id": book_id,
        "user_id": user_id,
        "due_date": due_date
    })

    return {"message": f"Book borrowed for {borrow_request.days} days"}