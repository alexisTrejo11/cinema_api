from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .services import WalletService
from .serializers import WalletSerializer, WalletTransactionSerializer
from django.core.exceptions import ValidationError

class WalletViewSet(viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = WalletSerializer
    wallet_service = WalletService()

    def get_serializer_class(self):
        if self.action in ['add_credit', 'make_purchase']:
            return WalletTransactionSerializer
        return super().get_serializer_class()

    @action(detail=False, methods=['GET'])
    def info(self, request):
        try:
            wallet = self.wallet_service.get_wallet(request.user)
            serializer = self.get_serializer(wallet)
            return Response({
                'message': 'Wallet information retrieved successfully',
                'data': serializer.data
            })
        except ValidationError as e:
            return Response({
                'message': str(e)
            }, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['POST'])
    def add_credit(self, request):
        try:
            amount = request.data.get('amount')
            wallet, transaction = self.wallet_service.add_credit(
                request.user, 
                amount
            )
            
            return Response({
                'message': 'Credit added successfully',
                'data': {
                    'new_balance': str(wallet.balance),
                    'transaction': WalletTransactionSerializer(transaction).data
                }
            })
        except ValidationError as e:
            return Response({
                'message': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

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