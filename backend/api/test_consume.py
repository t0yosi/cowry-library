import pika

def get_rabbitmq_connection():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='books')
    return connection, channel

def callback(ch, method, properties, body):
    print(f"Received message: {body.decode()}")

def consume_messages():
    connection, channel = get_rabbitmq_connection()
    channel.basic_consume(queue='books', on_message_callback=callback, auto_ack=True)
    print('Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == "__main__":
    consume_messages()
