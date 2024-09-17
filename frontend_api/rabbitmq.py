import pika
from database import db

def callback(ch, method, properties, body):
    print(f"Received {body}")
    message = body.decode('utf-8')

    if "New book added" in message:
        title = message.replace('New book added: ', '')
        # Insert the new book into the MongoDB 'books' collection
        db.books.insert_one({"title": title, "available": True})

    elif "Book removed" in message:
        title = message.replace('Book removed: ', '')
        # Remove the book from MongoDB
        db.books.delete_one({"title": title})

def consume_messages():
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
    channel = connection.channel()

    channel.queue_declare(queue='books')
    channel.basic_consume(queue='books', on_message_callback=callback, auto_ack=True)

    print('Waiting for messages...')
    channel.start_consuming()
