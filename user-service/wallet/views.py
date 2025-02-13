from rest_framework import status, viewsets
from drf_spectacular.utils import OpenApiResponse, extend_schema
from drf_spectacular.openapi import OpenApiTypes
from rest_framework.response import Response
from rest_framework.decorators import action
from .serializers import WalletTransactionSerializer
from .services import WalletService
from django.core.exceptions import ValidationError

class WalletViewSet(viewsets.GenericViewSet):
    wallet_service = WalletService()

    @extend_schema(
        operation_description="Make a purchase from wallet",
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
