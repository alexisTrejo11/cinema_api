from rest_framework import serializers
from .models import Payment, PaymentRefund, SalesReport
from .validators import PaymentValidator

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'
        read_only_fields = ('status', 'transaction_id', 'created_at', 'updated_at')
    
    def validate(self, data):
        PaymentValidator.validate_amount(data.get('amount'))
        
        if data.get('payment_method') == 'credit_card':
            PaymentValidator.validate_card_number(data.get('card_number'))
            PaymentValidator.validate_expiry_date(
                data.get('card_expiry_month'),
                data.get('card_expiry_year')
            )
        
        return data
    
class RefundSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentRefund
        fields = '__all__'
        read_only_fields = ('status', 'refund_transaction_id', 'created_at')


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesReport
        fields = '__all__'
        read_only_fields = ('status', 'refund_transaction_id', 'created_at')