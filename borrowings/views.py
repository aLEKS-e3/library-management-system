from rest_framework import viewsets

from books_service.models import Book
from borrowings.models import Borrowing
from borrowings.serializers import BorrowingListSerializer, BorrowingSerializer
from telegram_bot.script import send_borrowing_info


class BorrowingViewSet(viewsets.ModelViewSet):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingSerializer

    def get_queryset(self):
        return Borrowing.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return BorrowingListSerializer
        return self.serializer_class

    def create(self, request, *args, **kwargs):
        book = Book.objects.get(id=request.data.get("book"))
        email = self.request.user.email
        date = request.data.get("expected_return_date")

        text = f"New borrowing by {email}\nTook \"{book}\" book\nExpected return on {date}"
        send_borrowing_info(text)

        return super().create(request, *args, **kwargs)
