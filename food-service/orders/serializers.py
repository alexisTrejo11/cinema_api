from drf_spectacular.utils import extend_schema_serializer, OpenApiExample
from rest_framework import serializers
from .models import Order, OrderPromotion

@extend_schema_serializer(
    examples=[
        OpenApiExample(
            'Order Promotion Example',
            value={
                'promotion': {
                    'id': '550e8400-e29b-41d4-a716-446655440000',
                    'name': 'Summer Sale',
                    'discount_type': 'percentage',
                    'discount_value': 20.0
                },
                'discount_amount': 5.99
            },
            description='Example of an applied promotion on an order'
        )
    ]
)
class OrderPromotionSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderPromotion
        fields = ['promotion', 'discount_amount']

@extend_schema_serializer(
    examples=[
        OpenApiExample(
            'Order Example',
            value={
                'id': '550e8400-e29b-41d4-a716-446655440000',
                'user_id': 123,
                'items': [
                    {
                        'product_id': '550e8400-e29b-41d4-a716-446655440001',
                        'quantity': 2,
                        'unit_price': 5.99
                    }
                ],
                'combos': [
                    {
                        'combo_id': '550e8400-e29b-41d4-a716-446655440002',
                        'quantity': 1,
                        'unit_price': 9.99
                    }
                ],
                'subtotal': 21.97,
                'tax': 3.30,
                'total_price': 25.27,
                'status': 'pending',
                'created_at': '2023-10-05T12:00:00Z',
                'updated_at': '2023-10-05T12:00:00Z',
                'promotions': [
                    {
                        'promotion': {
                            'id': '550e8400-e29b-41d4-a716-446655440000',
                            'name': 'Summer Sale',
                            'discount_type': 'percentage',
                            'discount_value': 20.0
                        },
                        'discount_amount': 5.99
                    }
                ]
            },
            description='Example of an order with items, combos, and applied promotions'
        )
    ]
)
class OrderSerializer(serializers.ModelSerializer):
    promotions = OrderPromotionSerializer(source='orderpromotion_set', many=True, read_only=True)
    status = serializers.CharField(read_only=True)

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