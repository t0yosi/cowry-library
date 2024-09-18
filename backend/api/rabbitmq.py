import pika

def get_rabbitmq_connection():
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))  # Adjust if using Docker
        channel = connection.channel()
        channel.queue_declare(queue='books', durable=True)  # Ensure consistency
        return connection, channel
    except pika.exceptions.AMQPConnectionError as e:
        print(f"Error connecting to RabbitMQ: {e}")
        return None, None

def publish_message(message: str):
    connection, channel = get_rabbitmq_connection()
    if connection and channel:
        channel.basic_publish(exchange='', routing_key='books', body=message)
        connection.close()
