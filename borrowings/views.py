from rest_framework import viewsets

from borrowings.models import Borrowing
from borrowings.serializers import BorrowingListSerializer, BorrowingSerializer


class BorrowingViewSet(viewsets.ModelViewSet):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingSerializer

    def get_queryset(self):
        return Borrowing.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return BorrowingListSerializer
        return self.serializer_class