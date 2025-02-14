from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from models import Promotion
from serializers import PromotionSerializer
from services.promotion_service import PromotionService

@extend_schema(tags=['Promotions'])
class PromotionViewSet(viewsets.ViewSet):
    serializer_class = PromotionSerializer

    @extend_schema(
        description="List all active and valid promotions",
        responses={200: PromotionSerializer(many=True)}
    )
    def list(self, request):
        promotions = PromotionService.get_valid_promotions()
        serializer = self.serializer_class(promotions, many=True)
        return Response(serializer.data)

    @extend_schema(
        description="Create new promotion",
        request=PromotionSerializer,
        responses={201: PromotionSerializer}
    )
    def create(self, request):
        try:
            promotion = PromotionService.create_promotion(request.data)
            serializer = self.serializer_class(promotion)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        description="Apply promotion usage",
        methods=['POST'],
        responses={200: PromotionSerializer}
    )
    @action(detail=True, methods=['post'])
    def apply(self, request, pk=None):
        try:
            promotion = PromotionService.apply_promotion(pk)
            serializer = self.serializer_class(promotion)
            return Response(serializer.data)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Promotion.DoesNotExist:
            return Response({"error": "Promotion not found"}, status=status.HTTP_404_NOT_FOUND)