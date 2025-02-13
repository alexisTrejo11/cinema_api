from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Combo, Promotion
from .serializers import ComboSerializer, PromotionSerializer

class ComboViewSet(viewsets.ModelViewSet):
    queryset = Combo.objects.prefetch_related(
        'comboproduct_set__product'
    ).filter(is_active=True).order_by('-created_at')
    serializer_class = ComboSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['price', 'created_at']


class PromotionViewSet(viewsets.ModelViewSet):
    queryset = Promotion.objects.all().order_by('-start_date')
    serializer_class = PromotionSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['discount_type', 'products', 'combos']
    search_fields = ['name', 'description']

    def get_queryset(self):
        return self.queryset.prefetch_related('products', 'combos')
    
