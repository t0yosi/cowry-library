from pydantic import BaseModel, Field
from typing import Optional

class User(BaseModel):
    email: str
    first_name: str
    last_name: str

class Book(BaseModel):
    title: str
    publisher: str
    category: str
    is_borrowed: bool = False
    due_date: Optional[str] = None  # Date when the book will be available if borrowed

class BookFilter(BaseModel):
    publisher: Optional[str] = Field(None, description="Filter by publisher")
    category: Optional[str] = Field(None, description="Filter by category")