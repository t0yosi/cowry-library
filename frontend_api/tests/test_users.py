import pytest
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_enroll_user():
    response = client.post(
        "/users/",
        json={"email": "test@example.com", "first_name": "John", "last_name": "Doe"},
    )
    assert response.status_code == 200

