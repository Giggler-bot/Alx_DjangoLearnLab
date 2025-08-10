# advanced-api-project/api/test_views.py

from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from .models import Author, Book

class BookAPITestCase(APITestCase):

    def setUp(self):
        # Create a user and a token for authenticated requests
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.token = Token.objects.create(user=self.user)
        self.auth_headers = {'HTTP_AUTHORIZATION': f'Token {self.token.key}'}

        # Create an author and a book for testing
        self.author = Author.objects.create(name='Test Author')
        self.book = Book.objects.create(
            title='Test Book',
            publication_year=2020,
            author=self.author
        )
        self.book_list_url = reverse('book-list-create')
        self.book_detail_url = reverse('book-detail', kwargs={'pk': self.book.pk})

    def test_book_list(self):
        """Test that an unauthenticated user can list books."""
        response = self.client.get(self.book_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_book_authenticated(self):
        """Test that an authenticated user can create a book."""
        data = {
            'title': 'New Book',
            'publication_year': 2023,
            'author': self.author.pk
        }
        response = self.client.post(self.book_list_url, data, format='json', **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_delete_book_unauthenticated(self):
        """Test that an unauthenticated user cannot delete a book."""
        response = self.client.delete(self.book_detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)