import pika

def get_rabbitmq_connection():
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
    channel = connection.channel()
    channel.queue_declare(queue='books')
    return connection, channel

def publish_message(message: str):
    connection, channel = get_rabbitmq_connection()
    channel.basic_publish(exchange='', routing_key='books', body=message)
    connection.close()

if __name__ == "__main__":
    publish_message('Hello RabbitMQ!')
    print('Message published.')
