from fastapi import APIRouter
from models import User
from database import db
from rabbitmq import notify_user_enrolled

router = APIRouter()

@router.post("/")
async def enroll_user(user: User):
    # Add user to the database
    result = db.users.insert_one(user.dict())
    new_user_id = str(result.inserted_id)
    
    # Notify backend API about the new user
    notify_user_enrolled({
        "id": new_user_id,
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name
    })

    return {"message": "User enrolled successfully"}
