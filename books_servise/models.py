from django.db import models


class Book(models.Model):
    COVER = [
        ("HARD", ),
        ("SOFT", )
    ]

    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    cover = models.CharField(choices=COVER)
    inventory = models.PositiveIntegerField()
    daily_fee = models.DecimalField(max_digits=3, decimal_places=2)
