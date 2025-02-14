from django.core.cache import cache
from .models import Order, OrderPromotion
import logging

logger = logging.getLogger(__name__)

class OrderRepository:
    CACHE_TIMEOUT = 60 * 15  # 15 minutes
    
    @classmethod
    def _get_cache_key(cls, order_id):
        return f"order_{order_id}"

    @classmethod
    def create_order(cls, order_data):
        try:
            order = Order.objects.create(**order_data)
            logger.info(f"Order created: {order.id}")
            return order
        except Exception as e:
            logger.error(f"Order creation failed: {str(e)}")
            raise

    @classmethod
    def get_order(cls, order_id):
        cache_key = cls._get_cache_key(order_id)
        cached_order = cache.get(cache_key)
        if cached_order:
            logger.debug(f"Cache hit for order: {order_id}")
            return cached_order
            
        try:
            order = Order.objects.get(id=order_id)
            cache.set(cache_key, order, cls.CACHE_TIMEOUT)
            return order
        except Order.DoesNotExist as e:
            logger.warning(f"Order not found: {order_id}")
            raise
        except Exception as e:
            logger.error(f"Error retrieving order: {str(e)}")
            raise

    @classmethod
    def update_order_status(cls, order_id, new_status):
        try:
            order = Order.objects.get(id=order_id)
            order.status = new_status
            order.save()
            cache.delete(cls._get_cache_key(order_id))
            logger.info(f"Order {order_id} status updated to {new_status}")
            return order
        except Order.DoesNotExist as e:
            raise
        except Exception as e:
            logger.error(f"Error updating order status: {str(e)}")
            raise

    @classmethod
    def apply_promotion(cls, order_id, promotion):
        try:
            order = Order.objects.get(id=order_id)
            discount = promotion.calculate_discount(order.subtotal)
            OrderPromotion.objects.create(
                order=order,
                promotion=promotion,
                discount_amount=discount
            )
            logger.info(f"Promotion {promotion.id} applied to order {order_id}")
            return order
        except Exception as e:
            logger.error(f"Error applying promotion: {str(e)}")
            raise