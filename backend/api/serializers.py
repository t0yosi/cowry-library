from rest_framework import serializers
from .models import User, Book, BorrowRecord

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

class BorrowRecordSerializer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField()
    book_title = serializers.SerializerMethodField()

    class Meta:
        model = BorrowRecord
        fields = ['id', 'user', 'book', 'due_date', 'user_name', 'book_title']

    def get_user_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"

    def get_book_title(self, obj):
        return obj.book.title