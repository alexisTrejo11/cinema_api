from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from .models import Payment, SalesReport
from django.core.exceptions import ValidationError
from decimal import Decimal

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    permission_classes = [IsAuthenticated]
    
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        try:
            # Validate payment data
            amount = request.data.get('amount')
            if not amount or Decimal(amount) <= 0:
                raise ValidationError('Invalid amount')
                
            # Create payment record
            payment = Payment.objects.create(
                user_id=request.user.id,
                amount=amount,
                payment_method_id=request.data.get('payment_method'),
                booking_id=request.data.get('booking_id'),
                order_id=request.data.get('order_id'),
                ip_address=self.get_client_ip(request)
            )
            
            # Process payment with payment gateway
            payment_processor = self.get_payment_processor(payment.payment_method)
            result = payment_processor.process_payment(payment)
            
            # Update payment status based on result
            payment.status = result['status']
            payment.transaction_id = result.get('transaction_id', '')
            payment.payment_details = result
            payment.save()
            
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
        payment = self.get_object()
        
        if payment.status != 'completed':
            return Response({
                'status': 'error',
                'message': 'Only completed payments can be refunded'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            amount = Decimal(request.data.get('amount', payment.amount))
            if amount > payment.amount - payment.refund_amount:
                raise ValidationError('Refund amount exceeds available amount')
            
            # Process refund with payment gateway
            payment_processor = self.get_payment_processor(payment.payment_method)
            result = payment_processor.process_refund(payment, amount)
            
            # Create refund record
            refund = PaymentRefund.objects.create(
                payment=payment,
                amount=amount,
                reason=request.data.get('reason', ''),
                status='processed' if result['success'] else 'failed',
                refund_transaction_id=result.get('refund_transaction_id', ''),
                processed_by=request.user.id
            )
            
            # Update payment status and refund amount
            payment.refund_amount += amount
            payment.status = 'partially_refunded' if payment.refund_amount < payment.amount else 'refunded'
            payment.save()
            
            return Response({
                'status': 'success',
                'refund_id': refund.id
            })
            
        except Exception as e:
            return Response({
                'status': 'error',
                'message': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        return request.META.get('REMOTE_ADDR')

class SalesReportViewSet(viewsets.ModelViewSet):
    queryset = SalesReport.objects.all()
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['post'])
    def generate(self, request):
        try:
            start_date = request.data.get('start_date')
            end_date = request.data.get('end_date')
            report_type = request.data.get('report_type')
            
            report = SalesReport.objects.create(
                start_date=start_date,
                end_date=end_date,
                report_type=report_type,
                generated_by=request.user.id
            )
            
            # Trigger async task to generate report
            # generate_sales_report.delay(report.id)
            
            return Response({
                'status': 'success',
                'report_id': report.reference_id
            })
            
        except Exception as e:
            return Response({
                'status': 'error',
                'message': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)