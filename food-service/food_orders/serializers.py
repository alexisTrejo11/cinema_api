from rest_framework import serializers
from .models import Product, Order

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'category', 'image_url', 'is_available']

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'user_id', 'items', 'total_price', 'status', 'created_at']

    def validate_items(self, value):
        for item in value:
            if not isinstance(item.get('quantity'), int) or item['quantity'] < 1:
                raise serializers.ValidationError("Invalid quantity for product")
        return value