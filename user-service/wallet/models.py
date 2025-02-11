from django.db import models
from django.conf import settings

user = settings.AUTH_USER_MODEL

class TransactionType(models.TextChoices):
    DEPOSIT = 'DEPOSIT', 'Deposit'
    PURCHASE = 'PURCHASE', 'Purchase'
    Refund = 'Refund', 'Refund'
    

class CinemaWallet(models.Model):
    user = models.OneToOneField(user, on_delete=models.CASCADE, unique=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Wallet for {self.user.email}"


class WalletTransaction(models.Model):
    wallet = models.ForeignKey(CinemaWallet, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=20, choices=TransactionType.choices)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.transaction_type} - {self.amount} for {self.wallet.user.email}"
