import pika
import time
import logging
from pika.exceptions import AMQPConnectionError
from database import db


def callback(ch, method, properties, body):
    print(f"Received message: {body.decode('utf-8')}")
    message = body.decode("utf-8")
    if "New book added" in message:
        # Example message format: "New book added: Title by Publisher in Category"
        parts = message.replace("New book added: ", "").split(" by ")
        title = parts[0].strip()
        publisher_and_category = parts[1].split(" in ")
        publisher = publisher_and_category[0].strip()
        category = publisher_and_category[1].strip()
        
        # Insert the new book into the database
        result = db.books.insert_one({"title": title, "publisher": publisher, "category": category, "available": True})
        new_id = result.inserted_id

        print(f"New book inserted with ID: {new_id}")

        new_book = db.books.find_one({"_id": new_id})
        if new_book:
            print(f"Book inserted successfully: {new_book}")
        else:
            print("Book insertion failed.")
        
    elif "Book removed" in message:
        # Example message format: "Book removed: Title"
        title = message.replace("Book removed: ", "").strip()
        db.books.delete_one({"title": title})


def consume_messages():
    while True:
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters("rabbitmq"))
            channel = connection.channel()
            channel.queue_declare(queue="books", durable=True)  # Ensure consistency

            channel.basic_consume(
                queue="books", on_message_callback=callback, auto_ack=True
            )

            print("Waiting for messages...")
            channel.start_consuming()
        except AMQPConnectionError as e:
            logging.error(f"Connection failed: {e}. Retrying in 5 seconds...")
            time.sleep(5)
        except Exception as e:
            logging.error(f"Unexpected error: {e}")
            time.sleep(5)
