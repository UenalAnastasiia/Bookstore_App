from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from users.models import CustomUser
from .models import Book
from .serializers import BookSerializer
from rest_framework_simplejwt.tokens import AccessToken

class BookTests(APITestCase):

    def setUp(self):
        self.username = 'testuser'
        self.password = 'testpassword'
        self.user = CustomUser.objects.create_user(username=self.username, password=self.password)
        self.book = Book.objects.create(
            title='Test Book',
            description='A test book description',
            author=self.user,
            price=29.99,
            publish=True
        )
        self.access_token = AccessToken.for_user(self.user)

    def get_authorization_header(self):
        return f'Bearer {self.access_token}'

    def test_get_books_list(self):
        url = reverse('books-list')
        response = self.client.get(url, HTTP_AUTHORIZATION=self.get_authorization_header())
        books = Book.objects.filter(publish=True)
        serializer = BookSerializer(books, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_get_book_details(self):
        url = reverse('book-details', kwargs={'pk': self.book.id})
        response = self.client.get(url, HTTP_AUTHORIZATION=self.get_authorization_header())
        book = Book.objects.get(id=self.book.id)
        serializer = BookSerializer(book)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_create_book(self):
        url = reverse('books-list')
        data = {
            'title': 'New Test Book',
            'description': 'A new test book description',
            'author': self.user.id,
            'price': 39.99,
            'publish': True
        }
        response = self.client.post(url, data, format='json', HTTP_AUTHORIZATION=self.get_authorization_header())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 2)
        self.assertEqual(Book.objects.get(id=response.data['id']).title, 'New Test Book')

    # def test_update_book(self):
    #     url = reverse('book-details', kwargs={'pk': self.book.id})
    #     data = {'title': 'Updated Test Book'}
    #     response = self.client.patch(url, data, format='json', HTTP_AUTHORIZATION=self.get_authorization_header())
    #     self.book.refresh_from_db()
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(self.book.title, 'Updated Test Book')

    # def test_delete_book(self):
    #     url = reverse('book-details', kwargs={'pk': self.book.id})
    #     response = self.client.delete(url, HTTP_AUTHORIZATION=self.get_authorization_header())
    #     self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    #     self.assertFalse(Book.objects.filter(id=self.book.id).exists())