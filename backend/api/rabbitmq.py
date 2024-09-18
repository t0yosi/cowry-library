import pika
import time
from django.db import transaction
from .models import User, Book, BorrowRecord
from pika.exceptions import AMQPConnectionError


def get_rabbitmq_connection():
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))  # Adjust if using Docker
        channel = connection.channel()
        # Declare all queues here to ensure they exist
        channel.queue_declare(queue='books', durable=True)
        channel.queue_declare(queue='users', durable=True)
        channel.queue_declare(queue='borrows', durable=True)
        return connection, channel
    except pika.exceptions.AMQPConnectionError as e:
        print(f"Error connecting to RabbitMQ: {e}")
        return None, None

def publish_message(message: str, queue: str):
    print(f"Publishing message to {queue}: {message}")
    connection, channel = get_rabbitmq_connection()
    if connection and channel:
        channel.basic_publish(exchange='', routing_key=queue, body=message)
        connection.close()

# Callback function to handle messages from RabbitMQ
def callback(ch, method, properties, body):
    message = body.decode('utf-8')
    print(f"Received message: {message}")

    if "User enrolled" in message:
        user_data = eval(message.replace("User enrolled: ", "").strip())  # Be cautious with eval
        with transaction.atomic():
            # Add user to backend's database
            user = User(id=str(user_data["id"]), email=user_data["email"], first_name=user_data["first_name"], last_name=user_data["last_name"])
            user.save()
            print(f"New user enrolled in backend: {user_data}")

    elif "Book borrowed" in message:
        borrow_data = eval(message.replace("Book borrowed: ", "").strip())  # Be cautious with eval
        with transaction.atomic():
            # Create a new borrow record
            borrow_record = BorrowRecord.objects.create(**borrow_data)
            print(f"New borrow record created: {borrow_record}")

def consume_messages():
    while True:
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
            channel = connection.channel()
            channel.queue_declare(queue='users', durable=True)
            channel.queue_declare(queue='borrows', durable=True)

            channel.basic_consume(queue='users', on_message_callback=callback, auto_ack=True)
            channel.basic_consume(queue='borrows', on_message_callback=callback, auto_ack=True)

            print("Waiting for messages...")
            channel.start_consuming()
        except AMQPConnectionError as e:
            print(f"Connection failed: {e}")
            time.sleep(5)
        except Exception as e:
            print(f"Unexpected error: {e}")
            time.sleep(5)
