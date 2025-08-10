# advanced-api-project/api/test_views.py

from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from .models import Author, Book

class BookAPITestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.token = Token.objects.create(user=self.user)
        self.auth_headers = {'HTTP_AUTHORIZATION': f'Token {self.token.key}'}

        self.author = Author.objects.create(name='Test Author')
        self.book = Book.objects.create(
            title='Test Book',
            publication_year=2020,
            author=self.author
        )
        self.book_list_url = reverse('book-list')
        self.book_create_url = reverse('book-create')
        self.book_detail_url = reverse('book-detail', kwargs={'pk': self.book.pk})
        self.book_update_url = reverse('book-update', kwargs={'pk': self.book.pk})
        self.book_delete_url = reverse('book-delete', kwargs={'pk': self.book.pk})

    def test_book_list(self):
        """Test that an unauthenticated user can list books."""
        response = self.client.get(self.book_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check that the response data is a list containing the book we created
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Test Book')

    def test_create_book_authenticated(self):
        """Test that an authenticated user can create a book."""
        data = {
            'title': 'New Book',
            'publication_year': 2023,
            'author': self.author.pk
        }
        response = self.client.post(self.book_create_url, data, format='json', **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Check that the new book's title is in the response data
        self.assertEqual(response.data['title'], 'New Book')

    def test_create_book_unauthenticated(self):
        """Test that an unauthenticated user cannot create a book."""
        data = {'title': 'New Book', 'publication_year': 2023, 'author': self.author.pk}
        response = self.client.post(self.book_create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_book_authenticated(self):
        """Test that an authenticated user can update a book."""
        updated_data = {'title': 'Updated Title', 'publication_year': 2021, 'author': self.author.pk}
        response = self.client.put(self.book_update_url, updated_data, format='json', **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check the response data to confirm the update
        self.assertEqual(response.data['title'], 'Updated Title')
        
    def test_delete_book_unauthenticated(self):
        """Test that an unauthenticated user cannot delete a book."""
        response = self.client.delete(self.book_delete_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.login