from .models import CinemaWallet, WalletTransaction, TransactionType
from django.db import transaction
from decimal import Decimal
from django.core.exceptions import ValidationError

class WalletService:
    def __init__(self):
        self.wallet_model = CinemaWallet
        self.transaction_model = WalletTransaction

    def init_wallet(self, user):
        new_wallet = CinemaWallet()
        new_wallet.user = user
        new_wallet.balance = 0
        new_wallet.save()

    def get_wallet(self, user):
        try:
            return self.wallet_model.objects.get(user=user)
        except self.wallet_model.DoesNotExist:
            raise ValidationError("Wallet not found")
        

    def validate_amount(self, amount):
        if not isinstance(amount, Decimal):
            try:
                amount = Decimal(str(amount))
            except:
                raise ValidationError("Invalid amount format")
        
        if amount <= 0:
            raise ValidationError("Amount must be positive")
        
        return amount

    @transaction.atomic
    def add_credit(self, user, amount):
        amount = self.validate_amount(amount)
        wallet = self.get_wallet(user)
        
        wallet.balance += amount
        wallet.save()

        transaction = self.transaction_model.objects.create(
            wallet=wallet,
            amount=amount,
            transaction_type=TransactionType.DEPOSIT,
            description=f'Credit added: ${amount}'
        )

        return wallet, transaction

    @transaction.atomic
    def make_purchase(self, user, amount, description):
        amount = self.validate_amount(amount)
        wallet = self.get_wallet(user)

        if not wallet.has_sufficient_funds(amount):
            raise ValidationError("Insufficient funds")

        wallet.balance -= amount
        wallet.save()

        transaction = self.transaction_model.objects.create(
            wallet=wallet,
            amount=-amount,
            transaction_type=TransactionType.PURCHASE,
            description=description
        )

        return wallet, transaction

