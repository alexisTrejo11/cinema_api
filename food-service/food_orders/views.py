from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Product, Order
from .serializers import ProductSerializer, OrderSerializer
import requests
from rest_framework.decorators import action
from django.conf import settings

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.filter(is_available=True)
    serializer_class = ProductSerializer

    @action(detail=False, methods=['get'], url_path='search')
    def search(self, request):
        queryset = Product.objects.all()
        name = request.query_params.get("name", None)
        category = request.query_params.get("category", None)
        min_price = request.query_params.get("min_price", None)
        max_price = request.query_params.get("max_price", None)
        is_available = request.query_params.get("is_available", None)


        if name:
            queryset = queryset.filter(name__icontains=name)
        if category:
            queryset = queryset.filter(category=category)
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        if is_available is not None:
            queryset = queryset.filter(is_available=is_available.lower() == "true")

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)



class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def create(self, request, *args, **kwargs):
        user_id = request.data.get('user_id')
        items = request.data.get('items', [])
        
        # Validate user exists
        try:
            response = requests.get(
                f"{settings.USER_SERVICE_URL}/api/users/{user_id}/",
                timeout=5
            )
            if response.status_code != 200:
                return Response(
                    {"error": "Invalid user ID"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
        except requests.exceptions.RequestException:
            return Response(
                {"error": "User service unavailable"},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )

        # Calculate total price and validate products
        total_price = 0
        for item in items:
            product_id = item.get('product_id')
            quantity = item.get('quantity', 1)
            
            try:
                product = Product.objects.get(id=product_id, is_available=True)
                total_price += product.price * quantity
            except Product.DoesNotExist:
                return Response(
                    {"error": f"Product {product_id} not available"},
                    status=status.HTTP_400_BAD_REQUEST
                )

        # Create order
        serializer = self.get_serializer(data={
            **request.data,
            "total_price": total_price
        })
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)