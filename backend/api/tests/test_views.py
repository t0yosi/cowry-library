from rest_framework.test import APITestCase
from rest_framework import status
from api.models import User, Book

class UserAPITest(APITestCase):

    def test_create_user(self):
        url = '/api/users/'
        data = {'email': 'testuser@example.com', 'first_name': 'Test', 'last_name': 'User'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)

class BookAPITest(APITestCase):

    def setUp(self):
        self.book = Book.objects.create(title="The Pragmatic Programmer", publisher="Addison-Wesley", category="Technology")

    def test_list_books(self):
        url = '/api/books/'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_book(self):
        url = '/api/books/'
        data = {'title': 'Clean Code', 'publisher': 'Prentice Hall', 'category': 'Technology'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 2)
