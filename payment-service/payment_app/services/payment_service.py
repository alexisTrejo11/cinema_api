from decimal import Decimal
from django.core.exceptions import ValidationError
from ..models import Payment, PaymentRefund
from ..validators import PaymentValidator
from .payment_processor_factory import PaymentProcessorFactory

class PaymentService:
    def __init__(self):
        self.validator = PaymentValidator()
        self.processor_factory = PaymentProcessorFactory()

    def create_payment(self, user_id, amount, payment_method_id, booking_id=None, 
                      order_id=None, ip_address=None):
        self.validator.validate_amount(amount)
        
        payment = Payment.objects.create(
            user_id=user_id,
            amount=amount,
            payment_method_id=payment_method_id,
            booking_id=booking_id,
            order_id=order_id,
            ip_address=ip_address
        )
        
        processor = self.processor_factory.get_processor(payment.payment_method)
        result = processor.process_payment(payment)
        
        self.__update_payment_status(payment, result)
        return payment

    def process_refund(self, payment, amount, reason, processed_by):
        if payment.status != 'completed':
            raise ValidationError('Only completed payments can be refunded')
            
        if amount > payment.amount - payment.refund_amount:
            raise ValidationError('Refund amount exceeds available amount')
        
        processor = self.processor_factory.get_processor(payment.payment_method)
        result = processor.process_refund(payment, amount)
        
        refund = self.__create_refund_record(payment, amount, reason, result, processed_by)
        self.__update_payment_after_refund(payment, amount)
        
        return refund

    def __update_payment_status(self, payment, result):
        payment.status = result['status']
        payment.transaction_id = result.get('transaction_id', '')
        payment.payment_details = result
        payment.save()

    def __create_refund_record(self, payment, amount, reason, result, processed_by):
        return PaymentRefund.objects.create(
            payment=payment,
            amount=amount,
            reason=reason,
            status='processed' if result['success'] else 'failed',
            refund_transaction_id=result.get('refund_transaction_id', ''),
            processed_by=processed_by
        )

    def __update_payment_after_refund(self, payment, refund_amount):
        payment.refund_amount += refund_amount
        payment.status = ('partially_refunded' 
                         if payment.refund_amount < payment.amount 
                         else 'refunded')
        payment.save()