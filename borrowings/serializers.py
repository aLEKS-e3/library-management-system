from rest_framework import serializers

from books_service.models import Book
from books_service.serializers import BookSerializer
from borrowings.models import Borrowing


class BorrowingSerializer(serializers.ModelSerializer):
    book = serializers.SerializerMethodField()

    class Meta:
        model = Borrowing
        fields = (
            "id",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "user_id",
            "book_id",
            "book"
        )

    def get_book(self, obj):
        book_id = obj.book_id
        book = Book.objects.get(id=book_id)
        book_serializer = BookSerializer(book)
        return book_serializer.data


class BorrowingListSerializer(BorrowingSerializer):

    class Meta:
        model = Borrowing
        fields = (
            "id",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book"
        )


class BorrowingDetailSerializer(BorrowingSerializer):

    class Meta:
        model = Borrowing
        fields = "__all__"
