from rest_framework import status, viewsets
from drf_spectacular.utils import OpenApiResponse, extend_schema
from drf_spectacular.openapi import OpenApiTypes
from rest_framework.response import Response
from rest_framework.decorators import action
from .serializers import WalletTransactionSerializer, WalletSerializer
from .services import WalletService
from .models import WalletTransaction
from django.core.exceptions import ValidationError


class WalletViewSet(viewsets.GenericViewSet):
    wallet_service = WalletService()

    @extend_schema(
        description="Get user's wallet details and recent transactions",
        responses={
            200: OpenApiResponse(
                description="Wallet details retrieved successfully",
                response={
                    'wallet': WalletSerializer,
                    'recent_transactions': WalletTransactionSerializer(many=True)
                }
            ),
            404: OpenApiResponse(
                description="Wallet not found",
                response={
                    'message': OpenApiTypes.STR,
                }
            ),
        }
    )
    @action(detail=False, methods=['GET'])
    def my_wallet(self, request):
        try:
            wallet = self.wallet_service.get_wallet(request.user)
            recent_transactions = WalletTransaction.objects.filter(
                wallet=wallet
            ).order_by('-created_at')[:10]

            return Response({
                'wallet': WalletSerializer(wallet).data,
                'recent_transactions': WalletTransactionSerializer(
                    recent_transactions, 
                    many=True
                ).data
            })
        except ValidationError as e:
            return Response({
                'message': str(e)
            }, status=status.HTTP_404_NOT_FOUND)

    # Your existing make_purchase method
    @extend_schema(
        description="Make a purchase from wallet",
        request=OpenApiResponse(
            description="Amount and optional description for purchase",
            response={
                'amount': OpenApiTypes.DECIMAL,
                'description': OpenApiTypes.STR,
            }
        ),
        responses={
            200: OpenApiResponse(
                description="Purchase completed successfully",
                response={
                    'message': OpenApiTypes.STR,
                    'data': {
                        'new_balance': OpenApiTypes.STR,
                        'transaction': WalletTransactionSerializer,
                    }
                }
            ),
            400: OpenApiResponse(
                description="Invalid amount format or insufficient funds",
                response={
                    'message': OpenApiTypes.STR,
                }
            ),
        }
    )
    @action(detail=False, methods=['POST'])
    def make_purchase(self, request):
        try:
            amount = request.data.get('amount')
            description = request.data.get('description', '')

            wallet, transaction = self.wallet_service.make_purchase(
                request.user,
                amount,
                description
            )

            return Response({
                'message': 'Purchase completed successfully',
                'data': {
                    'new_balance': str(wallet.balance),
                    'transaction': WalletTransactionSerializer(transaction).data
                }
            })
        except ValidationError as e:
            return Response({
                'message': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)