from fastapi import APIRouter
from models import Book
from database import db

router = APIRouter()

@router.get("/")
async def list_books():
    books = list(db.books.find({"available": True}, {"_id": 0}))
    return {"books": books}
