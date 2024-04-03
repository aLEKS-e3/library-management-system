from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from books_service.models import Book

BORROWINGS_URL = reverse("borrowings:borrowings-list")


class BorrowingCreateSerializerTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@test.test", password="test_password"
        )
        self.client.force_authenticate(self.user)

    def test_create_borrowing_with_invalid_data(self):
        book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            cover="HARD",
            inventory=0,
            daily_fee=10.0
        )
        payload = {
            "expected_return_date": "2024-04-05",
            "book": book.pk
        }

        res = self.client.post(BORROWINGS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_borrowing_with_valid_data(self):
        book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            cover="HARD",
            inventory=10,
            daily_fee=10.0
        )
        payload = {
            "expected_return_date": "2024-04-05",
            "book": book.pk
        }

        res = self.client.post(BORROWINGS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
