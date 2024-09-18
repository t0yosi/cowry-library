from fastapi import APIRouter
from models import User
from database import db

router = APIRouter()

@router.post("/")
async def enroll_user(user: User):
    db.users.insert_one(user.dict())
    return {"message": "User enrolled successfully"}
