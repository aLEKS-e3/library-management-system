from rest_framework import serializers

from books_service.models import Book
from books_service.serializers import BookSerializer
from borrowings.models import Borrowing


class BorrowingListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = "__all__"


class BorrowingDetailSerializer(serializers.ModelSerializer):
    book_id = serializers.PrimaryKeyRelatedField(queryset=Book.objects.all())

    class Meta:
        model = Borrowing
        fields = (
            "id",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "user_id",
            "book_id"
        )

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        book_id = representation.pop("book_id")
        book = Book.objects.get(pk=book_id)
        representation["book"] = BookSerializer(book).data
        return representation
