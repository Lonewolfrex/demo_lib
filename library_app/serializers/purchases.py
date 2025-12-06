from rest_framework import serializers
from library_app.models import Purchase, Book


class PurchaseSerializer(serializers.ModelSerializer):
    book = serializers.PrimaryKeyRelatedField(queryset=Book.objects.all())

    class Meta:
        model = Purchase
        fields = ["id", "book", "purchased_on"]
        read_only_fields = ["id", "purchased_on"]
