from rest_framework import serializers
from .models import Order, OrderPromotion

class OrderPromotionSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderPromotion
        fields = ['promotion', 'discount_amount']


class OrderSerializer(serializers.ModelSerializer):
    promotions = OrderPromotionSerializer(source='orderpromotion_set', many=True, read_only=True)
    status = serializers.CharField(read_only=True)  # Status should only be updated internally

    class Meta:
        model = Order
        fields = [
            'id', 'user_id', 'items', 'combos', 'subtotal', 'tax', 'total_price',
            'applied_promotions', 'status', 'created_at', 'updated_at', 'promotions'
        ]
        read_only_fields = ['subtotal', 'tax', 'total_price', 'created_at', 'updated_at']

    def validate_user_id(self, value):
        # Call the user microservice to validate the user_id
        # Example: requests.get(f'http://user-service/validate/{value}')
        # If invalid, raise serializers.ValidationError("Invalid user ID")
        return value

    def validate_items(self, value):
        for item in value:
            if not isinstance(item.get('product_id'), str) or not isinstance(item.get('quantity'), int):
                raise serializers.ValidationError("Invalid item format")
        return value

    def validate_combos(self, value):
        for combo in value:
            if not isinstance(combo.get('combo_id'), str) or not isinstance(combo.get('quantity'), int):
                raise serializers.ValidationError("Invalid combo format")
        return value

    def create(self, validated_data):
        order = Order(**validated_data)
        order.calculate_total()
        order.save()
        return order
