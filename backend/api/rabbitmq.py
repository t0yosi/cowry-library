import pika

def get_rabbitmq_connection():
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))  # 'rabbitmq' is the service name in docker-compose
    channel = connection.channel()
    channel.queue_declare(queue='books')  # Declare a queue named 'books'
    return connection, channel

def publish_message(message: str):
    connection, channel = get_rabbitmq_connection()
    channel.basic_publish(exchange='', routing_key='books', body=message)
    connection.close()
      