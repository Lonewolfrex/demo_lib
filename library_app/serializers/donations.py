from rest_framework import serializers
from library_app.models import Donation, Book


class DonationSerializer(serializers.ModelSerializer):
    book = serializers.PrimaryKeyRelatedField(queryset=Book.objects.all())

    class Meta:
        model = Donation
        fields = ["id", "book", "donated_on"]
        read_only_fields = ["id", "donated_on"]
