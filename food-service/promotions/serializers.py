from .models import ComboProduct, Combo, Promotion
from rest_framework import serializers
from products.serializers import ProductSerializer

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