from rest_framework import viewsets, permissions
from library_app.models import Book
from library_app.serializers import BookSerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all().order_by("id")
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]
