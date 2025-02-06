# views.py
from rest_framework import viewsets, filters, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Product, Combo, Promotion, Order, Payment, SalesReport
from .serializers import ProductSerializer, ComboSerializer, PromotionSerializer, OrderSerializer, PaymentSerializer, SalesReportSerializer
from rest_framework.decorators import action

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
    

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all().order_by('-created_at')
    serializer_class = OrderSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status', 'user_id']

    @action(detail=True, methods=['post'])
    def update_status(self, request, pk=None):
        order = self.get_object()
        new_status = request.data.get('status')
        if new_status not in dict(Order.STATUS_CHOICES):
            return Response({"error": "Invalid status"}, status=status.HTTP_400_BAD_REQUEST)
        order.status = new_status
        order.save()
        return Response({"status": order.status})


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all().order_by('-created_at')
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status', 'payment_method']


    def get_queryset(self):
        return self.queryset.filter(order__user_id=self.request.user.id)

    def perform_create(self, serializer):
        order = serializer.validated_data['order']
        if order.status != 'payment_pending':
            raise ValueError("Order is not in payment pending state")
        serializer.save()

class SalesReportViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SalesReport.objects.all().order_by('-start_date')
    serializer_class = SalesReportSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['report_type']
