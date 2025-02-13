from rest_framework import serializers
from drf_spectacular.utils import extend_schema_serializer
from .models import CinemaWallet, WalletTransaction

@extend_schema_serializer(
    examples=[
        {
            "id": 1,
            "amount": "100.00",
            "transaction_type": "DEPOSIT",
            "description": "Added funds to wallet",
            "created_at": "2025-02-12T10:00:00Z"
        }
    ]
)
class WalletTransactionSerializer(serializers.ModelSerializer):
    """
    Serializer for wallet transactions.

    Handles the serialization of transactions related to the user's wallet,
    including deposits, purchases, and refunds.
    """

    class Meta:
        model = WalletTransaction
        fields = ('id', 'amount', 'transaction_type', 'description', 'created_at')


@extend_schema_serializer(
    examples=[
        {
            "balance": "250.00",
            "recent_transactions": [
                {
                    "id": 1,
                    "amount": "100.00",
                    "transaction_type": "DEPOSIT",
                    "description": "Added funds to wallet",
                    "created_at": "2025-02-12T10:00:00Z"
                },
                {
                    "id": 2,
                    "amount": "-50.00",
                    "transaction_type": "PURCHASE",
                    "description": "Bought a movie ticket",
                    "created_at": "2025-02-12T12:30:00Z"
                }
            ]
        }
    ]
)
class WalletSerializer(serializers.ModelSerializer):
    """
    Serializer for the user's wallet.

    Includes the current wallet balance and a list of recent transactions.
    """

    recent_transactions = WalletTransactionSerializer(
        source='wallettransaction_set',
        many=True,
        read_only=True
    )

    class Meta:
        model = CinemaWallet
        fields = ('balance', 'recent_transactions')
