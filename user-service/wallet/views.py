from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from .models import CinemaWallet, WalletTransaction
from .serializers import WalletSerializer, WalletTransactionSerializer
from decimal import Decimal


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_wallet_info(request):
    try:
        wallet = request.user.cinemawallet
        serializer = WalletSerializer(wallet)
        return Response({
            'message': 'Wallet information retrieved successfully',
            'data': serializer.data
        })
    except CinemaWallet.DoesNotExist:
        return Response({
            'message': 'Wallet not found'
        }, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_credit(request):
    try:
        amount = Decimal(request.data.get('amount', 0))
        if amount <= 0:
            raise ValueError("Amount must be positive")

        with transaction.atomic():
            wallet = request.user.cinemawallet
            wallet.balance += amount
            wallet.save()

            transaction = WalletTransaction.objects.create(
                wallet=wallet,
                amount=amount,
                transaction_type='DEPOSIT',
                description=f'Credit added: ${amount}'
            )

            return Response({
                'message': 'Credit added successfully',
                'data': {
                    'new_balance': str(wallet.balance),
                    'transaction': WalletTransactionSerializer(transaction).data
                }
            })
    except (ValueError, Exception) as e:
        return Response({
            'message': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def make_purchase(request):
    try:
        amount = Decimal(request.data.get('amount', 0))
        description = request.data.get('description', '')

        if amount <= 0:
            raise ValueError("Amount must be positive")

        with transaction.atomic():
            wallet = request.user.cinemawallet
            if wallet.balance < amount:
                raise ValueError("Insufficient funds")

            wallet.balance -= amount
            wallet.save()

            transaction = WalletTransaction.objects.create(
                wallet=wallet,
                amount=-amount,
                transaction_type='PURCHASE',
                description=description
            )

            return Response({
                'message': 'Purchase completed successfully',
                'data': {
                    'new_balance': str(wallet.balance),
                    'transaction': WalletTransactionSerializer(transaction).data
                }
            })
    except (ValueError, Exception) as e:
        return Response({
            'message': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)
