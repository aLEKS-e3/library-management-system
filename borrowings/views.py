from datetime import date
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from borrowings.models import Borrowing
from borrowings.permissions import IsAdminOrIfAuthenticatedReadOnly
from borrowings.serializers import (
    BorrowingListSerializer,
    BorrowingSerializer
)


class BorrowingViewSet(viewsets.ModelViewSet):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingSerializer
    permission_classes = [IsAdminOrIfAuthenticatedReadOnly]

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
