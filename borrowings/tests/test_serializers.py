from django.contrib.auth import get_user_model
from django.test import TestCase

from books_service.models import Book
from borrowings.serializers import BorrowingSerializer


class BorrowingCreateSerializerTest(TestCase):
    def setUp(self):
        self.book_with_zero_samples = Book.objects.create(
            title="Test Book",
            author="Test Author",
            cover="HARD",
            inventory=0,
            daily_fee=10.0
        )
        self.book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            cover="HARD",
            inventory=10,
            daily_fee=10.0
        )
        self.user = get_user_model().objects.create_user(
            email="test@test.com",
            password="test_password"
        )

    def test_create_borrowing_with_invalid_data(self):
        payload = {
            "expected_return_date": "2024-04-05",
            "book": self.book_with_zero_samples.pk,
            "user": self.user.pk
        }

        serializer = BorrowingSerializer(data=payload)
        self.assertFalse(serializer.is_valid())

    def test_create_borrowing_with_valid_data(self):
        payload = {
            "expected_return_date": "2024-04-05",
            "book": self.book.pk,
            "user": self.user.pk
        }

        serializer = BorrowingSerializer(data=payload)
        self.assertTrue(serializer.is_valid())
