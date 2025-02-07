from abc import ABC, abstractmethod
from decimal import Decimal
import logging

logger = logging.getLogger(__name__)

class PaymentProcessor(ABC):
    @abstractmethod
    def process_payment(self, payment):
        pass
    
    @abstractmethod
    def process_refund(self, payment, amount):
        pass

class CreditCardProcessor(PaymentProcessor):
    def process_payment(self, payment):
        logger.info(f"Processing credit card payment {payment.reference_id}")
        return {
            'success': True,
            'transaction_id': f'CC-{payment.reference_id}',
            'status': 'completed'
        }
    
    def process_refund(self, payment, amount):
        logger.info(f"Processing refund for payment {payment.reference_id}")
        return {
            'success': True,
            'refund_transaction_id': f'RF-{payment.reference_id}'
        }
