from rest_framework import serializers
from library_app.models import Rental, Book


class RentalSerializer(serializers.ModelSerializer):
    book = serializers.PrimaryKeyRelatedField(queryset=Book.objects.all())

    class Meta:
        model = Rental
        fields = ["id", "book", "rented_on", "returned_on"]
        read_only_fields = ["id", "rented_on", "returned_on"]
