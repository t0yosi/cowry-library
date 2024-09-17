from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    email: str
    first_name: str
    last_name: str

class Book(BaseModel):
    title: str
    publisher: str
    category: str
    available: bool = True
    due_date: Optional[str] = None  # Date when the book will be available if borrowed
