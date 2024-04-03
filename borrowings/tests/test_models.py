from django.contrib.auth import get_user_model
from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils import timezone

from books_service.models import Book
from borrowings.models import Borrowing


class BorrowingModelTest(TestCase):
    def setUp(self):
        self.book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            cover="Test Cover",
            inventory=20,
            daily_fee=20.0

        )
        self.user = get_user_model().objects.create_user(
            email="test@test.com",
            password="test"
        )

    def test_valid_borrowing(self):
        """
        Test that a Borrowing object with valid dates does not raise any validation errors.
        """
        borrowing = Borrowing(
            borrow_date=timezone.now(),
            expected_return_date=timezone.now() + timezone.timedelta(days=7),
            actual_return_date=None,
            book=self.book,
            user=self.user,
        )
        # This should not raise any validation errors
        borrowing.full_clean()

    def test_invalid_expected_return_date(self):
        """
        Test that an invalid expected return date raises a validation error.
        """
        borrowing = Borrowing(
            borrow_date=timezone.now(),
            expected_return_date=timezone.now() - timezone.timedelta(days=7),
            actual_return_date=None,
            book=self.book,
            user=self.user
        )
        with self.assertRaises(ValidationError):
            borrowing.full_clean()

    def test_invalid_actual_return_date(self):
        """
        Test that an invalid actual return date raises a validation error.
        """
        borrowing = Borrowing(
            borrow_date=timezone.now(),
            expected_return_date=timezone.now() + timezone.timedelta(days=7),
            actual_return_date=timezone.now() - timezone.timedelta(days=7),
            book=self.book,
            user=self.user
        )
        with self.assertRaises(ValidationError):
            borrowing.full_clean()

    def test_valid_actual_return_date(self):
        """
        Test that providing an actual return date after the borrow date does not raise any validation errors.
        """
        borrowing = Borrowing(
            borrow_date=timezone.now() - timezone.timedelta(days=7),
            expected_return_date=timezone.now(),
            actual_return_date=timezone.now(),
            book=self.book,
            user=self.user
        )
        borrowing.full_clean()
