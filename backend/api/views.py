from rest_framework import viewsets, serializers
from .models import User, Book, BorrowRecord
from .serializers import UserSerializer, BookSerializer, BorrowRecordSerializer
from .rabbitmq import publish_message, consume_messages
import threading
from django.db import transaction

# Create your views here.

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def perform_create(self, serializer):
        title = serializer.validated_data['title']
        publisher = serializer.validated_data['publisher']
        category = serializer.validated_data['category']
        
        # Check if the book with the same title and publisher already exists
        if Book.objects.filter(title=title, publisher=publisher).exists():
            raise serializers.ValidationError("This book already exists.")
        
        # If not a duplicate, save the new book
        book = serializer.save()

        # Publish a message to RabbitMQ including the UUID of the book
        message = f'New book added: {book.title} by {book.publisher} in {book.category} with id {book.id}'
        publish_message(message, queue='books')  # Specify the queue name if needed

    def perform_destroy(self, instance):
        # Publish a message before removing the book
        publish_message(f'Book removed: {instance.title}')
        instance.delete()


class BorrowRecordViewSet(viewsets.ModelViewSet):
    queryset = BorrowRecord.objects.all()
    serializer_class = BorrowRecordSerializer

    def perform_create(self, serializer):
        book = serializer.validated_data['book']

        if book.is_borrowed:
            raise serializers.ValidationError("This book is already borrowed.")
        
        # Mark the book as borrowed and save the record
        with transaction.atomic():
            book.is_borrowed = True
            book.save()
            serializer.save()

    def perform_destroy(self, instance):
        # Mark the book as available
        with transaction.atomic():
            instance.book.is_borrowed = False
            instance.book.save()
            instance.delete()

# Start a background thread to listen for RabbitMQ messages
def start_consumer():
    thread = threading.Thread(target=consume_messages)
    thread.daemon = True
    thread.start()
    print('waiting...')

# Call this at app startup (e.g., in apps.py or manage.py)
start_consumer()
