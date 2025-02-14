from django.core.cache import cache
from models import Combo, ComboProduct
import logging

logger = logging.getLogger(__name__)

class ComboRepository:
    CACHE_TIMEOUT = 60 * 15  # 15 minutes
    
    @classmethod
    def _get_cache_key(cls, combo_id):
        return f"combo_{combo_id}"

    @classmethod
    def get_active_combos(cls):
        cache_key = "active_combos"
        cached = cache.get(cache_key)
        if cached:
            logger.debug("Cache hit for active combos")
            return cached
            
        combos = Combo.objects.prefetch_related('comboproduct_set__product').filter(is_active=True).order_by('-created_at')
        cache.set(cache_key, combos, cls.CACHE_TIMEOUT)
        return combos

    @classmethod
    def create_combo(cls, combo_data, products_data):
        try:
            combo = Combo.objects.create(**combo_data)
            for product_data in products_data:
                ComboProduct.objects.create(
                    combo=combo,
                    product_id=product_data['product_id'],
                    quantity=product_data['quantity']
                )
            cache.delete("active_combos")
            logger.info(f"Combo created: {combo.id}")
            return combo
        except Exception as e:
            logger.error(f"Combo creation failed: {str(e)}")
            raise

    @classmethod
    def get_combo_by_id(cls, combo_id):
        cache_key = cls._get_cache_key(combo_id)
        cached = cache.get(cache_key)
        if cached:
            return cached
            
        combo = Combo.objects.prefetch_related('comboproduct_set__product').get(id=combo_id)
        cache.set(cache_key, combo, cls.CACHE_TIMEOUT)
        return combo

    @classmethod
    def update_combo_status(cls, combo_id, is_active):
        try:
            combo = Combo.objects.get(id=combo_id)
            combo.is_active = is_active
            combo.save()
            cache.delete_many([cls._get_cache_key(combo_id), "active_combos"])
            return combo
        except Combo.DoesNotExist:
            raise