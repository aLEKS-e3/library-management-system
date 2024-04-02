from rest_framework import viewsets

from books_service.models import Book
from books_service.serializers import BookSerializer
# from books_service.permissions import IsAdminOrReadOnly


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    # permission_classes = (IsAdminOrReadOnly, )
