from rest_framework import viewsets
from .models import User, Book, BorrowRecord
from .serializers import UserSerializer, BookSerializer, BorrowRecordSerializer
from .rabbitmq import publish_message

# Create your views here.

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def perform_create(self, serializer):
        # Save the new book
        book = serializer.save()
        
        # Publish a message to RabbitMQ
        publish_message(f'New book added: {book.title}')

    def perform_destroy(self, instance):
        # Publish a message before removing the book
        publish_message(f'Book removed: {instance.title}')
        instance.delete()

class BorrowRecordViewSet(viewsets.ModelViewSet):
    queryset = BorrowRecord.objects.all()
    serializer_class = BorrowRecordSerializer
