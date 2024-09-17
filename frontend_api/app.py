from fastapi import FastAPI
from routes import books, users
import threading
from rabbitmq import consume_messages


app = FastAPI()

# Include the routes from different files
app.include_router(users.router, prefix="/users")
app.include_router(books.router, prefix="/books")

# Start a background thread to listen for RabbitMQ messages
def start_consumer():
    thread = threading.Thread(target=consume_messages)
    thread.daemon = True
    thread.start()


start_consumer()