import pytest
from fastapi.testclient import TestClient
from app import app
from database import db
from bson import ObjectId

client = TestClient(app)

@pytest.fixture(autouse=True)
def clear_db():
    db.books.delete_many({})  # Clear books collection before each test

def test_list_books():
    # Insert test data
    db.books.insert_many([
        {"title": "Book 1", "publisher": "Wiley", "category": "Technology", "is_borrowed": True},
        {"title": "Book 2", "publisher": "Apress", "category": "Fiction", "is_borrowed": False}
    ])
    
    response = client.get("/books/")
    assert response.status_code == 200
    books = response.json()
    assert isinstance(books, dict)
    assert "books" in books
    assert len(books["books"]) == 1  # Only one book should be available

def test_get_book_by_id():
    # Insert test data
    book_id = str(db.books.insert_one({"title": "Book 1", "publisher": "Wiley", "category": "Technology", "is_borrowed": True}).inserted_id)
    
    response = client.get(f"/books/{book_id}")
    assert response.status_code == 200
    book = response.json()
    assert book["title"] == "Book 1"
    
    # Test invalid ID
    response = client.get("/books/invalid_id")
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid ID format"}
    
    # Test non-existent book ID
    response = client.get("/books/641b29c19f1b8c02b8477b7c")  # Use an invalid ObjectId here
    assert response.status_code == 404
    assert response.json() == {"detail": "Book not found"}

def test_filter_books_by_publisher():
    db.books.delete_many({})  # Clear any previous data
    db.books.insert_many([
        {"title": "Book 1", "publisher": "Wiley", "category": "Technology", "is_borrowed": True},
        {"title": "Book 2", "publisher": "Apress", "category": "Fiction", "is_borrowed": True}
    ])
    
    response = client.get("/books/filter/?publisher=Wiley")
    assert response.status_code == 200
    books = response.json()
    assert isinstance(books, dict)
    assert "books" in books
    assert len(books["books"]) == 1
    assert books["books"][0]["publisher"] == "Wiley"

def test_filter_books_by_category():
    db.books.delete_many({})  # Clear any previous data
    db.books.insert_many([
        {"title": "Book 1", "publisher": "Wiley", "category": "Technology", "is_borrowed": True},
        {"title": "Book 2", "publisher": "Apress", "category": "Fiction", "is_borrowed": True}
    ])
    
    response = client.get("/books/filter/?category=Fiction")
    assert response.status_code == 200
    books = response.json()
    assert isinstance(books, dict)
    assert "books" in books
    assert len(books["books"]) == 1
    assert books["books"][0]["category"] == "Fiction"


def test_borrow_book():
    # Insert a book into the database
    book_id = str(db.books.insert_one({
        "title": "Book 1",
        "publisher": "Wiley",
        "category": "Technology",
        "is_borrowed": False
    }).inserted_id)

    # Make the POST request
    response = client.post(
        f"/books/{book_id}/borrow",
        json={"days": 7}
    )

    # Check if the status code is 200 OK
    assert response.status_code == 200
    assert response.json() == {"message": "Book borrowed for 7 days"}

