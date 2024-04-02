from datetime import date, timedelta
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.core.exceptions import ValidationError

from books_service.models import Book
from borrowings.models import Borrowing


class BorrowingModelTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            email="email@mail.com",
            password="111222"
        )
        self.book = Book.objects.create(
            title="Big boobs",
            author="Big Bob",
            cover="Hard cover",
            inventory=24,
            daily_fee=100
        )

    def test_valid_borrowing(self):
        """
        Test that a Borrowing object with valid dates does not raise any validation errors.
        """
        borrowing = Borrowing(
            borrow_date=date.today(),
            expected_return_date=date.today() + timedelta(days=7),
            actual_return_date=None,
            book=self.book,
            user=self.user
        )
        # This should not raise any validation errors
        borrowing.full_clean()

    def test_invalid_expected_return_date(self):
        """
        Test that an invalid expected return date raises a validation error.
        """
        borrowing = Borrowing(
            borrow_date=date.today(),
            expected_return_date=date.today() - timedelta(days=7),
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
            borrow_date=date.today(),
            expected_return_date=date.today() + timedelta(days=7),
            actual_return_date=date.today() - timedelta(days=7),
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
            borrow_date=date.today() - timedelta(days=7),
            expected_return_date=date.today(),
            actual_return_date=date.today(),
            book=self.book,
            user=self.user
        )
        borrowing.full_clean()
