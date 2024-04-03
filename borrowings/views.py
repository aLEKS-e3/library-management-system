from datetime import date
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import status, mixins
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from books_service.models import Book
from borrowings.models import Borrowing
from borrowings.serializers import (
    BorrowingSerializer,
    BorrowingListSerializer,
)
from telegram_bot.script import send_borrowing_info


class BorrowingViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    GenericViewSet
):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingSerializer
    permission_classes = [IsAuthenticated]

    @staticmethod
    def _params_to_ints(qs):
        """Converts a list of string IDs to a list of integers"""
        return [int(str_id) for str_id in qs.split(",") if str_id]

    def get_queryset(self):
        queryset = self.queryset
        is_active_param = self.request.query_params.get("is_active")
        user_id_param = self.request.query_params.get("user_id")

        if is_active_param:
            queryset = queryset.filter(actual_return_date=None)

        if not self.request.user.is_superuser:
            return queryset.filter(user=self.request.user)

        if user_id_param:
            user_id = self._params_to_ints(user_id_param)

            if user_id:
                queryset = queryset.filter(user__id__in=user_id)

        return queryset

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return BorrowingListSerializer

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
        url_path="return",
        permission_classes=[IsAuthenticated]
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

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "is_active",
                type={"type": "list", "items": {"type": "any"}},
                description="Filter borrowings by status (eg. ?is_active=)"
            ),
            OpenApiParameter(
                "user_id",
                type={"type": "list", "items": {"type": "number"}},
                description=(
                    "Admin user ids filter "
                    "for borrowings (eg. ?user_id=1,3)")
            )
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
