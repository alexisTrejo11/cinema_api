from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Seat, Booking
from .serializers import SeatSerializer, BookingSerializer
import requests
from django.conf import settings

class SeatViewSet(viewsets.ModelViewSet):
    queryset = Seat.objects.all()
    serializer_class = SeatSerializer

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

    def create(self, request, *args, **kwargs):
        showtime_id = request.data.get('showtime_id')
        seats = request.data.get('seats', [])

        # Validate the showtime with Billboard Service
        try:
            response = requests.get(
                f"{settings.BILLBOARD_SERVICE_URL}/api/showtimes/{showtime_id}/",
                timeout=5  # Timeout after 5 seconds
            )
            if response.status_code != 200:
                return Response(
                    {"error": "Invalid showtime ID"},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except requests.exceptions.RequestException as e:
            return Response(
                {"error": f"Failed to connect to Billboard Service: {str(e)}"},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )

        # Check seat availability
        for seat_id in seats:
            seat = Seat.objects.filter(id=seat_id, is_reserved=False).first()
            if not seat:
                return Response(
                    {"error": f"Seat {seat_id} is already reserved or invalid"},
                    status=status.HTTP_400_BAD_REQUEST
                )

        # Step 3: Create the booking
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)