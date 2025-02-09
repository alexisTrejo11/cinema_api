from rest_framework import serializers
from .models import CinemaWallet, WalletTransaction

class WalletTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = WalletTransaction
        fields = ('id', 'amount', 'transaction_type', 'description', 'created_at')

class WalletSerializer(serializers.ModelSerializer):
    recent_transactions = WalletTransactionSerializer(
        source='wallettransaction_set',
        many=True,
        read_only=True
    )

    class Meta:
        model = CinemaWallet
        fields = ('balance', 'recent_transactions')