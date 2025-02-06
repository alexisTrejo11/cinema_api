# views.py
from rest_framework import viewsets, filters, permissions
from django_filters.rest_framework import DjangoFilterBackend
from .models import Product, Combo, Promotion
from .serializers import ProductSerializer, ComboSerializer, PromotionSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().order_by('-created_at')
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'is_available']
    search_fields = ['name', 'description']
    ordering_fields = ['price', 'created_at', 'stock_quantity']

    def get_queryset(self):
        queryset = super().get_queryset()
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')
        
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        return queryset


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