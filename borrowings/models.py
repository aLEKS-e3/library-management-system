from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models

from books_service.models import Book


class Borrowing(models.Model):
    borrow_date = models.DateField(auto_now_add=True)
    expected_return_date = models.DateField()
    actual_return_date = models.DateField(null=True, blank=True)
    book = models.ForeignKey(
        to=Book,
        on_delete=models.CASCADE,
        related_name="borrowings"
    )
    user = models.ForeignKey(
        to=get_user_model(),
        on_delete=models.CASCADE,
        related_name="borrowings"
    )

    def clean(self):
        if self.borrow_date > self.expected_return_date:
            raise ValidationError("Expected return date must be after borrow date")
        if self.actual_return_date and self.actual_return_date < self.borrow_date:
            raise ValidationError("Actual return date must be after borrow date")

    def __str__(self):
        return (f"Book: {self.book}, User: {self.user},"
                f" {self.borrow_date} - {self.expected_return_date}")
