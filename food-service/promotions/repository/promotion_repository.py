from django.core.cache import cache
from ..models import Promotion
import logging
from django.utils import timezone

logger = logging.getLogger(__name__)

class PromotionRepository:
    CACHE_TIMEOUT = 60 * 30  # 30 minutes
    
    @classmethod
    def get_active_promotions(cls):
        cache_key = "active_promotions"
        cached = cache.get(cache_key)
        if cached:
            logger.debug("Cache hit for active promotions")
            return cached
            
        now = timezone.now()
        promotions = Promotion.objects.filter(
            start_date__lte=now,
            end_date__gte=now
        ).prefetch_related('products', 'combos')
        cache.set(cache_key, promotions, cls.CACHE_TIMEOUT)
        return promotions

    @classmethod
    def create_promotion(cls, promotion_data):
        try:
            promotion = Promotion.objects.create(**promotion_data)
            cache.delete("active_promotions")
            logger.info(f"Promotion created: {promotion.id}")
            return promotion
        except Exception as e:
            logger.error(f"Promotion creation failed: {str(e)}")
            raise

    @classmethod
    def apply_promotion_usage(cls, promotion_id):
        try:
            promotion = Promotion.objects.get(id=promotion_id)
            promotion.current_usage += 1
            promotion.save()
            cache.delete("active_promotions")
            return promotion
        except Promotion.DoesNotExist:
            raise