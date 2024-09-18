import pika
import time
import logging
from pika.exceptions import AMQPConnectionError
from database import db

def callback(ch, method, properties, body):
    print(f"Received message: {body.decode('utf-8')}")
    message = body.decode("utf-8")
    if "New book added" in message:
        title = message.replace("New book added: ", "")
        db.books.insert_one({"title": title, "available": True})
    elif "Book removed" in message:
        title = message.replace("Book removed: ", "")
        db.books.delete_one({"title": title})

def consume_messages():
    while True:
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
            channel = connection.channel()
            channel.queue_declare(queue="books", durable=True)  # Ensure consistency

            channel.basic_consume(
                queue="books",
                on_message_callback=callback,
                auto_ack=True
            )

            print("Waiting for messages...")
            channel.start_consuming()
        except AMQPConnectionError as e:
            logging.error(f"Connection failed: {e}. Retrying in 5 seconds...")
            time.sleep(5)
        except Exception as e:
            logging.error(f"Unexpected error: {e}")
            time.sleep(5)
