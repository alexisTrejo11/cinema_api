from django.core.exceptions import ValidationError
from decimal import Decimal
import re

class PaymentValidator:
    @staticmethod
    def validate_amount(amount):
        try:
            amount = Decimal(str(amount))
            if amount <= 0:
                raise ValidationError("Amount must be greater than 0")
            if amount > Decimal('999999.99'):
                raise ValidationError("Amount exceeds maximum allowed")
        except (ValueError, TypeError):
            raise ValidationError("Invalid amount format")

    @staticmethod
    def validate_card_number(card_number):
        if not card_number or not re.match(r'^\d{16}$', card_number):
            raise ValidationError("Invalid card number")
    
    @staticmethod
    def validate_expiry_date(month, year):
        from datetime import datetime
        current_date = datetime.now()
        if not (1 <= int(month) <= 12):
            raise ValidationError("Invalid month")
        if datetime(int(year), int(month), 1) < current_date:
            raise ValidationError("Card has expired")