from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Payment
from .serializers import PaymentSerializer
import requests
from django.conf import settings

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    def create(self, request, *args, **kwargs):
        user_id = request.data.get('user_id')
        booking_id = request.data.get('booking_id')
        amount = request.data.get('amount')

        # Validate user exists
        try:
            user_response = requests.get(
                f"{settings.USER_SERVICE_URL}/api/users/{user_id}/",
                timeout=5
            )
            if user_response.status_code != 200:
                return Response(
                    {"error": "Invalid user ID"},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except requests.exceptions.RequestException as e:
            return Response(
                {"error": f"User service unavailable: {str(e)}"},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )

        # Validate booking exists
        try:
            booking_response = requests.get(
                f"{settings.TICKET_SERVICE_URL}/api/bookings/{booking_id}/",
                timeout=5
            )
            if booking_response.status_code != 200:
                return Response(
                    {"error": "Invalid booking ID"},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except requests.exceptions.RequestException as e:
            return Response(
                {"error": f"Ticket service unavailable: {str(e)}"},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )

        # Create payment
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)