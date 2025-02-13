from rest_framework import serializers
from .models import Product, Combo, ComboProduct, Promotion

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = ('created_at',)

class ComboProductSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    
    class Meta:
        model = ComboProduct
        fields = ('product', 'quantity')

class ComboSerializer(serializers.ModelSerializer):
    products = ComboProductSerializer(source='comboproduct_set', many=True, read_only=True)
    savings = serializers.SerializerMethodField()
    
    class Meta:
        model = Combo
        fields = '__all__'
        read_only_fields = ('created_at', 'savings')

    def get_savings(self, obj):
        total = sum(
            cp.quantity * cp.product.price 
            for cp in obj.comboproduct_set.select_related('product').all()
        )
        return float(total - obj.price)

class PromotionSerializer(serializers.ModelSerializer):
    is_valid = serializers.SerializerMethodField()
    
    class Meta:
        model = Promotion
        fields = '__all__'
        read_only_fields = ('current_usage', 'created_at', 'is_valid')

    def get_is_valid(self, obj):
        return obj.is_valid()

    def validate(self, data):
        if data['discount_type'] == 'percentage' and data['discount_value'] > 100:
            raise serializers.ValidationError("Percentage discount cannot exceed 100%")
        if data['start_date'] > data['end_date']:
            raise serializers.ValidationError("End date must be after start date")
        return data
    
from rest_framework import serializers
from .models import Product, Combo, ComboProduct, Promotion, Order,  OrderPromotion, Payment, SalesReport
from rest_framework import serializers
from decimal import Decimal

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = ('created_at',)

class ComboProductSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    
    class Meta:
        model = ComboProduct
        fields = ('product', 'quantity')

class ComboSerializer(serializers.ModelSerializer):
    products = ComboProductSerializer(source='comboproduct_set', many=True, read_only=True)
    savings = serializers.SerializerMethodField()
    
    class Meta:
        model = Combo
        fields = '__all__'
        read_only_fields = ('created_at', 'savings')

    def get_savings(self, obj):
        total = sum(
            cp.quantity * cp.product.price 
            for cp in obj.comboproduct_set.select_related('product').all()
        )
        return float(total - obj.price)


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
