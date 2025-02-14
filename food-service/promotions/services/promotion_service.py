from ..repository.promotion_repository import PromotionRepository
from django.utils import timezone

class PromotionService:
    @classmethod
    def validate_promotion(cls, promotion):
        now = timezone.now()
        return (
            promotion.start_date <= now <= promotion.end_date and
            (promotion.usage_limit is None or promotion.current_usage < promotion.usage_limit)
        )

    @classmethod
    def get_valid_promotions(cls):
        promotions = PromotionRepository.get_active_promotions()
        return [p for p in promotions if cls.validate_promotion(p)]

    @classmethod
    def apply_promotion(cls, promotion_id):
        try:
            promotion = PromotionRepository.apply_promotion_usage(promotion_id)
            if not cls.validate_promotion(promotion):
                raise ValueError("Promotion no longer valid")
            return promotion
        except Exception as e:
            raise