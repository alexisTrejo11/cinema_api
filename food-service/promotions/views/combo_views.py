from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from models import Combo
from serializers import ComboSerializer
from services import ComboService

@extend_schema(tags=['Combos'])
class ComboViewSet(viewsets.ViewSet):
    serializer_class = ComboSerializer

    @extend_schema(
        description="List active combos with product details",
        responses={200: ComboSerializer(many=True)}
    )
    def list(self, request):
        combos = ComboService.get_active_combos()
        serializer = self.serializer_class(combos, many=True)
        return Response(serializer.data)

    @extend_schema(
        description="Create new combo",
        request=ComboSerializer,
        responses={201: ComboSerializer}
    )
    def create(self, request):
        try:
            combo = ComboService.create_combo(
                request.data['name'],
                request.data['description'],
                request.data['price'],
                request.data['products']
            )
            serializer = self.serializer_class(combo)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        description="Toggle combo activation status",
        methods=['PATCH'],
        responses={200: ComboSerializer}
    )
    @action(detail=True, methods=['patch'])
    def toggle_active(self, request, pk=None):
        try:
            combo = ComboService.toggle_combo_status(pk, request.data.get('is_active', True))
            serializer = self.serializer_class(combo)
            return Response(serializer.data)
        except Combo.DoesNotExist:
            return Response({"error": "Combo not found"}, status=status.HTTP_404_NOT_FOUND)