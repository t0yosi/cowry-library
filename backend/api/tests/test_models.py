from django.test import TestCase
from .models import User, Book, BorrowRecord
from datetime import date

class UserModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(email='testuser@example.com', first_name='Test', last_name='User')

    def test_user_creation(self):
        self.assertEqual(self.user.email, 'testuser@example.com')
        self.assertEqual(self.user.first_name, 'Test')
        self.assertEqual(self.user.last_name, 'User')

class BookModelTest(TestCase):

    def setUp(self):
        self.book = Book.objects.create(title="The Pragmatic Programmer", publisher="Addison-Wesley", category="Technology")

    def test_book_creation(self):
        self.assertEqual(self.book.title, "The Pragmatic Programmer")
        self.assertEqual(self.book.publisher, "Addison-Wesley")
        self.assertEqual(self.book.category, "Technology")
        self.assertFalse(self.book.is_borrowed)

class BorrowRecordModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(email='borrower@example.com', first_name='Borrower', last_name='Test')
        self.book = Book.objects.create(title="Clean Code", publisher="Prentice Hall", category="Technology")
        self.borrow_record = BorrowRecord.objects.create(user=self.user, book=self.book, due_date=date.today())

    def test_borrow_record_creation(self):
        self.assertEqual(self.borrow_record.user.email, 'borrower@example.com')
        self.assertEqual(self.borrow_record.book.title, 'Clean Code')
        self.assertEqual(self.borrow_record.due_date, date.today())
