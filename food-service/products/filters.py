import django_filters
from .models import Product

class ProductFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name='price', lookup_expr='lte')

    class Meta:
        model = Product
        fields = {
            'category': ['exact'],
            'is_available': ['exact'],
            'price': ['gte', 'lte']
        }
