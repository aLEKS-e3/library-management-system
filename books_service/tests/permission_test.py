from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIRequestFactory
from books_service.models import Book
from books_service.permissions import IsAdminOrReadOnly
from books_service.views import BookViewSet


LIST_URL = "/books/"
RETRIEVE_URL = LIST_URL + "f'/books/{book.id}/'"


class PermissionsTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.book = Book.objects.create(
            title='Test Book',
            author='Test Author',
            cover='HARD',
            inventory=10,
            daily_fee=5.99)
        self.admin_user = get_user_model().objects.create_user(
            email='admin@admin.com',
            password='adminpass', is_staff=True
        )
        self.normal_user = get_user_model().objects.create_user(
            email='user@user.com',
            password='userpass'
        )

    def test_read_only_for_unauthenticated_user(self):
        request = self.factory.get('/books/')
        request.user = None
        permission = IsAdminOrReadOnly()
        self.assertTrue(permission.has_permission(request, BookViewSet()))

    def test_read_only_for_authenticated_user(self):
        request = self.factory.get('/books/')
        request.user = self.normal_user
        permission = IsAdminOrReadOnly()
        self.assertTrue(permission.has_permission(request, BookViewSet()))

    def test_read_write_for_admin_user(self):
        request = self.factory.post(LIST_URL)
        request.user = self.admin_user
        permission = IsAdminOrReadOnly()
        self.assertTrue(permission.has_permission(request, BookViewSet()))

    def test_read_only_for_unauthenticated_user_detail(self):
        book = self.book
        request = self.factory.get(RETRIEVE_URL)
        request.user = None
        permission = IsAdminOrReadOnly()
        self.assertTrue(permission.has_permission(request, BookViewSet()))

    def test_read_only_for_authenticated_user_detail(self):
        book = self.book
        request = self.factory.get(RETRIEVE_URL)
        request.user = self.normal_user
        permission = IsAdminOrReadOnly()
        self.assertTrue(permission.has_permission(request, BookViewSet()))

    def test_read_write_for_admin_user_detail(self):
        book = self.book
        request = self.factory.post(RETRIEVE_URL)
        request.user = self.admin_user
        permission = IsAdminOrReadOnly()
        self.assertTrue(permission.has_permission(request, BookViewSet()))
