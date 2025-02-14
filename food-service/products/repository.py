from django.core.cache import cache
from django.db import models
from .models import Product

import logging


logger = logging.getLogger(__name__)

class BaseRepository:
    model = None
    CACHE_TIMEOUT = 60 * 15  # 15 min
    
    @classmethod
    def get_cached(cls, key):
        return cache.get(key)
    
    @classmethod
    def set_cache(cls, key, data):
        try:
            cache.set(key, data, cls.CACHE_TIMEOUT)
        except Exception as e:
            logger.error(f"Error setting cache: {str(e)}")

class ProductRepository(BaseRepository):
    model = Product
    
    @classmethod
    def get_products(cls, filters=None):
        cache_key = f'products_{filters}'
        cached_data = cls.get_cached(cache_key)
        
        if cached_data:
            logger.info('Retrieving products from cache')
            return cached_data
        
        try:
            queryset = cls.model.objects.all().order_by('-created_at')
            if filters:
                queryset = filters.filter(queryset)
            cls.set_cache(cache_key, queryset)
            return queryset
        except Exception as e:
            logger.error(f"Database error: {str(e)}")
            raise