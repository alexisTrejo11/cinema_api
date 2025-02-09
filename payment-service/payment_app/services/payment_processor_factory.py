from abc import ABC, abstractmethod
import logging
from django.core.exceptions import ValidationError

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
        # Aquí iría la integración real con el gateway de pago
        return {
            'status': 'completed',
            'transaction_id': f'CC-{payment.reference_id}',
            'success': True
        }

    def process_refund(self, payment, amount):
        logger.info(f"Processing credit card refund for payment {payment.reference_id}")
        return {
            'success': True,
            'refund_transaction_id': f'RF-CC-{payment.reference_id}'
        }

class PayPalProcessor(PaymentProcessor):
    def process_payment(self, payment):
        logger.info(f"Processing PayPal payment {payment.reference_id}")
        return {
            'status': 'completed',
            'transaction_id': f'PP-{payment.reference_id}',
            'success': True
        }

    def process_refund(self, payment, amount):
        logger.info(f"Processing PayPal refund for payment {payment.reference_id}")
        return {
            'success': True,
            'refund_transaction_id': f'RF-PP-{payment.reference_id}'
        }

class CinemaWalletProcessor(PaymentProcessor):
    def process_payment(self, payment):
        logger.info(f"Processing wallet payment {payment.reference_id}")
 
        #TODO:Refund Wallet
        
        return {
            'status': 'completed',
            'transaction_id': f'WL-{payment.reference_id}',
            'success': True
        }

    def process_refund(self, payment, amount):
        logger.info(f"Processing wallet refund for payment {payment.reference_id}")
        return {
            'success': True,
            'refund_transaction_id': f'RF-WL-{payment.reference_id}'
        }

class PaymentProcessorFactory:    
    def __init__(self):
        self._processors = {
            'credit_card': CreditCardProcessor(),
            'paypal': PayPalProcessor(),
            'cinema_wallet': CinemaWalletProcessor()
        }

    def get_processor(self, payment_method):
        """
        Get the appropriate payment processor for the payment method
        
        Args:
            payment_method: PaymentMethod model instance
        
        Returns:
            PaymentProcessor: The appropriate processor instance
        
        Raises:
            ValidationError: If payment method is not supported
        """
        processor = self._processors.get(payment_method.name.lower())
        
        if not processor:
            raise ValidationError(f'Unsupported payment method: {payment_method.name}')
            
        return processor

    def register_processor(self, payment_method_name, processor):
        """
        Register a new payment processor
        
        Args:
            payment_method_name: String name of the payment method
            processor: PaymentProcessor instance
        """
        if not isinstance(processor, PaymentProcessor):
            raise ValueError("Processor must inherit from PaymentProcessor")
            
        self._processors[payment_method_name.lower()] = processor