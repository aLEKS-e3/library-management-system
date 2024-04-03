from django.db import models

from borrowings.models import Borrowing


class Payment(models.Model):
    STATUS_CHOICES = (
        ("PENDING", "Pending"),
        ("PAID", "Paid"),
    )
    TYPE_CHOICES = (
        ("PAYMENT", "Payment"),
        ("FINE", "Fine"),
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    borrowing = models.ForeignKey(Borrowing, on_delete=models.CASCADE, related_name="payments")
    session_url = models.URLField()
    session_id = models.CharField(max_length=100)
    money_to_pay = models.DecimalField(
        max_digits=10, decimal_places=2
    )

    def __str__(self):
        return (f"{self.get_status_display()} - {self.get_type_display()}"
                f" - Borrowing ID: {self.borrowing_id}")
