from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils import timezone
from borrowings.models import Borrowing


class BorrowingModelTest(TestCase):
    def test_valid_borrowing(self):
        """
        Test that a Borrowing object with valid dates does not raise any validation errors.
        """
        borrowing = Borrowing(
            borrow_date=timezone.now(),
            expected_return_date=timezone.now() + timezone.timedelta(days=7),
            actual_return_date=None,
            book_id=1,
            user_id=1
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
            book_id=1,
            user_id=1
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
            book_id=1,
            user_id=1
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
            book_id=1,
            user_id=1
        )
        borrowing.full_clean()
