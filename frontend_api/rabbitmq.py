import pika
import time
import logging
from pika.exceptions import AMQPConnectionError
from database import db

# Define a function to get RabbitMQ connection
def get_rabbitmq_connection():
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()
        channel.queue_declare(queue='books', durable=True)
        channel.queue_declare(queue='users', durable=True)
        channel.queue_declare(queue='borrows', durable=True)
        return connection, channel
    except pika.exceptions.AMQPConnectionError as e:
        print(f"Error connecting to RabbitMQ: {e}")
        return None, None

# Define a function to publish messages to RabbitMQ
def publish_message(message: str, queue: str):
    connection, channel = get_rabbitmq_connection()
    if connection and channel:
        channel.basic_publish(exchange='', routing_key=queue, body=message)
        connection.close()

# Functions to notify about user enrollment and book borrowing
def notify_user_enrolled(user_data):
    message = f"User enrolled: {user_data}"
    publish_message(message, 'users')

def notify_book_borrowed(borrow_data):
    message = f"Book borrowed: {borrow_data}"
    publish_message(message, 'borrows')

# Callback function to process received messages
def callback(ch, method, properties, body):
    print(f"Received message: {body.decode('utf-8')}")
    message = body.decode("utf-8")

    if "New book added" in message:
        # Split the message to extract book details
        parts = message.replace("New book added: ", "").split(" by ")
        title = parts[0].strip()
        
        # Further split to get publisher and category
        publisher_and_category_and_id = parts[1].split(" in ")
        publisher = publisher_and_category_and_id[0].strip()
        
        # Extract category and UUID from the message
        category_and_id = publisher_and_category_and_id[1].split(" with id ")
        category = category_and_id[0].strip()
        uuid = category_and_id[1].strip()
        
        # Insert the new book into MongoDB, including the UUID
        result = db.books.insert_one({
            "title": title,
            "publisher": publisher,
            "category": category,
            "uuid": uuid,  # Store the UUID
            "is_borrowed": False
        })
        
        new_id = result.inserted_id
        print(f"New book inserted with MongoDB ID: {new_id}, UUID: {uuid}")

        # new_book = db.books.find_one({"_id": new_id})
        # if new_book:
        #     print(f"Book inserted successfully: {new_book}")
        # else:
        #     print("Book insertion failed.")
        
    elif "Book removed" in message:
        title = message.replace("Book removed: ", "").strip()
        db.books.delete_one({"title": title})


# Function to start consuming messages from RabbitMQ
def consume_messages():
    while True:
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
            channel = connection.channel()
            channel.queue_declare(queue='books', durable=True)
            channel.basic_consume(queue='books', on_message_callback=callback, auto_ack=True)
            print("Waiting for messages...")
            channel.start_consuming()
        except AMQPConnectionError as e:
            logging.error(f"Connection failed: {e}. Retrying in 5 seconds...")
            time.sleep(5)
        except Exception as e:
            logging.error(f"Unexpected error: {e}")
            time.sleep(5)