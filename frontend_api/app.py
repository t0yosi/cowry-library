from fastapi import FastAPI
from routes import books, users

app = FastAPI()

# Include the routes from different files
app.include_router(users.router, prefix="/users")
app.include_router(books.router, prefix="/books")
