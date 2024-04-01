from django.core.exceptions import ValidationError
from django.db import models


class Borrowing(models.Model):
    borrow_date = models.DateField()
    expected_return_date = models.DateField()
    actual_return_date = models.DateField(null=True, blank=True)
    book_id = models.PositiveIntegerField()
    user_id = models.PositiveIntegerField()

    def clean(self):
        if self.borrow_date > self.expected_return_date:
            raise ValidationError("Expected return date must be after borrow date")
        if self.actual_return_date and self.actual_return_date < self.borrow_date:
            raise ValidationError("Actual return date must be after borrow date")