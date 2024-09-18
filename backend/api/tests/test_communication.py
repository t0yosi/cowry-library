import pika
from django.test import TestCase
from api.models import Book
from api.rabbitmq import publish_message

class RabbitMQIntegrationTest(TestCase):

    def setUp(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='books')

    def test_publish_message(self):
        # Create a new book and trigger publish
        book = Book.objects.create(title="RabbitMQ Book", publisher="Publisher", category="Technology")
        publish_message(f'New book added: {book.title}')
        
        # Check if message was sent to RabbitMQ
        method_frame, header_frame, body = self.channel.basic_get(queue='books', auto_ack=True)
        self.assertIsNotNone(method_frame)
        self.assertIn("New book added: RabbitMQ Book", body.decode())
