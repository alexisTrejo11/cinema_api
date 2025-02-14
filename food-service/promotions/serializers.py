from drf_spectacular.utils import extend_schema_serializer, OpenApiExample
from .models import ComboProduct, Combo, Promotion
from rest_framework import serializers
from products.serializers import ProductSerializer

@extend_schema_serializer(
    examples=[
        OpenApiExample(
            'Combo Product Example',
            value={
                'product': {
                    'id': '550e8400-e29b-41d4-a716-446655440000',
                    'name': 'Burger',
                    'price': 5.99
                },
                'quantity': 2
            },
            description='Example of a combo product relationship'
        )
    ]
)
class ComboProductSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    
    class Meta:
        model = ComboProduct
        fields = ('product', 'quantity')

@extend_schema_serializer(
    examples=[
        OpenApiExample(
            'Combo Example',
            value={
                'id': '550e8400-e29b-41d4-a716-446655440000',
                'name': 'Meal Deal',
                'description': 'Burger, fries, and drink',
                'price': 9.99,
                'is_active': True,
                'image_url': 'https://example.com/image.jpg',
                'created_at': '2023-10-05T12:00:00Z',
                'products': [
                    {
                        'product': {
                            'id': '550e8400-e29b-41d4-a716-446655440000',
                            'name': 'Burger',
                            'price': 5.99
                        },
                        'quantity': 1
                    },
                    {
                        'product': {
                            'id': '550e8400-e29b-41d4-a716-446655440001',
                            'name': 'Fries',
                            'price': 2.99
                        },
                        'quantity': 1
                    }
                ],
                'savings': 3.99
            },
            description='Example of a combo with products and calculated savings'
        )
    ]
)
class ComboSerializer(serializers.ModelSerializer):
    products = ComboProductSerializer(source='comboproduct_set', many=True, read_only=True)
    savings = serializers.SerializerMethodField()
    
    class Meta:
        model = Combo
        fields = '__all__'
        read_only_fields = ('created_at', 'savings')

    @extend_schema(
        description="Calculate the savings compared to buying products individually",
        responses={200: float}
    )
    def get_savings(self, obj):
        total = sum(
            cp.quantity * cp.product.price 
            for cp in obj.comboproduct_set.select_related('product').all()
        )
        return float(total - obj.price)

@extend_schema_serializer(
    examples=[
        OpenApiExample(
            'Promotion Example',
            value={
                'id': '550e8400-e29b-41d4-a716-446655440000',
                'name': 'Summer Sale',
                'description': '20% off all burgers',
                'discount_type': 'percentage',
                'discount_value': 20.0,
                'start_date': '2023-06-01T00:00:00Z',
                'end_date': '2023-08-31T23:59:59Z',
                'min_purchase_amount': 10.0,
                'usage_limit': 100,
                'current_usage': 0,
                'is_valid': True,
                'created_at': '2023-05-15T12:00:00Z'
            },
            description='Example of a percentage-based promotion'
        ),
        OpenApiExample(
            'Fixed Amount Promotion',
            value={
                'id': '550e8400-e29b-41d4-a716-446655440001',
                'name': '$5 Off Combo',
                'description': '$5 off any combo meal',
                'discount_type': 'fixed',
                'discount_value': 5.0,
                'start_date': '2023-10-01T00:00:00Z',
                'end_date': '2023-10-31T23:59:59Z',
                'min_purchase_amount': 15.0,
                'usage_limit': None,
                'current_usage': 0,
                'is_valid': True,
                'created_at': '2023-09-25T12:00:00Z'
            },
            description='Example of a fixed amount promotion'
        )
    ]
)
class PromotionSerializer(serializers.ModelSerializer):
    is_valid = serializers.SerializerMethodField()
    
    class Meta:
        model = Promotion
        fields = '__all__'
        read_only_fields = ('current_usage', 'created_at', 'is_valid')

    @extend_schema(
        description="Check if promotion is currently valid",
        responses={200: bool}
    )
    def get_is_valid(self, obj):
        return obj.is_valid()

    @extend_schema(
        description="Validate promotion data",
        responses={
            400: {
                "description": "Validation Error",
                "examples": {
                    "percentage_exceeded": {
                        "value": {"error": "Percentage discount cannot exceed 100%"}
                    },
                    "invalid_dates": {
                        "value": {"error": "End date must be after start date"}
                    }
                }
            }
        }
    )
    def validate(self, data):
        if data['discount_type'] == 'percentage' and data['discount_value'] > 100:
            raise serializers.ValidationError("Percentage discount cannot exceed 100%")
        if data['start_date'] > data['end_date']:
            raise serializers.ValidationError("End date must be after start date")
        return data