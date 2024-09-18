from rest_framework import viewsets, serializers
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
        title = serializer.validated_data['title']
        publisher = serializer.validated_data['publisher']
        
        if Book.objects.filter(title=title, publisher=publisher).exists():
            raise serializers.ValidationError("This book already exists.")
        
        # If not duplicate = Save the new book
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

    def perform_create(self, serializer):
        book = serializer.validated_data['book']

        if book.is_borrowed:
            raise serializers.ValidationError("This book is already borrowed.")
        
        # Mark the book as borrowed and save the record
        book.is_borrowed = True
        book.save()
        serializer.save()

    def perform_destroy(self, instance):
        # Mark the book as available
        instance.book.is_borrowed = False
        instance.book.save()
        
        instance.delete()

