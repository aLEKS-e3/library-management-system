from django.db import transaction
from rest_framework import serializers

from books_service.serializers import BookSerializer
from borrowings.models import Borrowing
from user.serializers import UserSerializer


class BorrowingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Borrowing
        fields = (
            "id",
            "borrow_date",
            "expected_return_date",
            "book",
            "user"
        )


class BorrowingListSerializer(BorrowingSerializer):
    user = UserSerializer(read_only=True)
    book = BookSerializer(read_only=True)

    class Meta:
        model = Borrowing
        fields = (
            "id",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book",
            "user"
        )


class BorrowingCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Borrowing
        fields = ("expected_return_date", "book")

    def validate_book(self, value):
        if value.inventory <= 0:
            raise serializers.ValidationError("Book inventory is 0. Cannot borrow.")
        return value

    def create(self, validated_data):
        with transaction.atomic():
            book = validated_data("book")
            borrowing = Borrowing.objects.create(**validated_data)
            book.inventory -= 1
            book.save()
            return borrowing
