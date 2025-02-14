from drf_spectacular.utils import extend_schema_serializer, OpenApiExample
from rest_framework import serializers
from .models import Product

@extend_schema_serializer(
    examples=[
        OpenApiExample(
            'Product Example',
            value={
                'id': '550e8400-e29b-41d4-a716-446655440000',
                'name': 'Cheeseburger',
                'description': 'A delicious cheeseburger with all the fixings',
                'price': 5.99,
                'category': 'meals',
                'image_url': 'https://example.com/cheeseburger.jpg',
                'is_available': True,
                'created_at': '2023-10-05T12:00:00Z',
                'stock_quantity': 100,
                'cost_price': 3.50
            },
            description='Example of a product with all fields'
        ),
        OpenApiExample(
            'Minimal Product Example',
            value={
                'name': 'Fries',
                'description': 'Crispy golden fries',
                'price': 2.99,
                'category': 'snacks',
                'is_available': True
            },
            description='Example of a product with only required fields'
        )
    ]
)
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = ('created_at',)

    def validate(self, data):
        # Example validation logic
        if data.get('price', 0) < 0:
            raise serializers.ValidationError("Price cannot be negative")
        return data