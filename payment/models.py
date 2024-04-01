from django.db import models


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
    borrowing_id = models.IntegerField()
    session_url = models.URLField()
    session_id = models.CharField(max_length=100)
    money_to_pay = models.DecimalField(
        max_digits=10, decimal_places=2
    )

    def __str__(self):
        return f"{self.get_status_display()} - {self.get_type_display()} - Borrowing ID: {self.borrowing_id}"
