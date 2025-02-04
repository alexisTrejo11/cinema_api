from rest_framework import serializers
from .models import Seat, Booking

class SeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seat
        fields = ['id', 'theater_id', 'seat_number', 'seat_type', 'is_reserved']

class BookingSerializer(serializers.ModelSerializer):
    seats = SeatSerializer(many=True, read_only=True)

    class Meta:
        model = Booking
        fields = ['id', 'user_id', 'showtime_id', 'seats', 'total_price', 'status', 'created_at']