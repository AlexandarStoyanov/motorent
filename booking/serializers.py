from rest_framework import serializers
from .models import Booking

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ["id", "motorcycle", "full_name", "email", "phone_number", "start_date", "end_date", "created_at"]
        read_only_fields = ["id", "created_at"]
