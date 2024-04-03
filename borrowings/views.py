from datetime import date
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from books_service.models import Book
from borrowings.models import Borrowing
from borrowings.serializers import BorrowingListSerializer, BorrowingSerializer, BorrowingCreateSerializer
from telegram_bot.script import send_borrowing_info


class BorrowingViewSet(viewsets.ModelViewSet):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingSerializer

    def get_queryset(self):
        return Borrowing.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return BorrowingListSerializer
        
        if self.action == "create":
            return BorrowingCreateSerializer
        return self.serializer_class

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
      
    def create(self, request, *args, **kwargs):
        book = Book.objects.get(id=request.data.get("book"))
        email = self.request.user.email
        date = request.data.get("expected_return_date")

        text = f"New borrowing by {email}\nTook \"{book}\" book\nExpected return on {date}"
        send_borrowing_info(text)

        return super().create(request, *args, **kwargs)

    @action(
        methods=["POST"],
        detail=True,
        url_path="return"
    )
    def return_borrowing(self, request, pk=None):
        borrowing = get_object_or_404(Borrowing, pk=pk)

        if borrowing.actual_return_date:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        borrowing.actual_return_date = date.today()
        borrowing.book.inventory += 1

        borrowing.save()
        borrowing.book.save()

        return Response(status=status.HTTP_204_NO_CONTENT)
