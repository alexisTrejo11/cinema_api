from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from ..services.payment_service import PaymentService
from ..serializers import PaymentSerializer
from ..models import Payment
from ..utils.request_utils import get_client_ip
from decimal import Decimal

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.payment_service = PaymentService()
    
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        try:
            payment = self.payment_service.create_payment(
                user_id=request.user.id,
                amount=request.data.get('amount'),
                payment_method_id=request.data.get('payment_method'),
                booking_id=request.data.get('booking_id'),
                order_id=request.data.get('order_id'),
                ip_address=get_client_ip(request)
            )
            
            return Response({
                'status': 'success',
                'payment_id': payment.reference_id,
                'transaction_id': payment.transaction_id
            })
            
        except Exception as e:
            return Response({
                'status': 'error',
                'message': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'])
    @transaction.atomic
    def refund(self, request, pk=None):
        try:
            payment = self.get_object()
            refund = self.payment_service.process_refund(
                payment=payment,
                amount=Decimal(request.data.get('amount', payment.amount)),
                reason=request.data.get('reason', ''),
                processed_by=1 #request.user.id
            )
            
            return Response({
                'status': 'success',
                'refund_id': refund.id
            })
            
        except Exception as e:
            return Response({
                'status': 'error',
                'message': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)