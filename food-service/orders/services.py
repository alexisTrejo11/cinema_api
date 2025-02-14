from decimal import Decimal
from repository import OrderRepository
from promotions.services import PromotionService

class OrderService:
    TAX_RATE = Decimal('0.15')

    @classmethod
    def create_order(cls, user_id, items, combos):
        order_data = {
            'user_id': user_id,
            'items': items,
            'combos': combos,
            'subtotal': Decimal('0'),
            'tax': Decimal('0'),
            'total_price': Decimal('0')
        }
        order = OrderRepository.create_order(order_data)
        return cls.calculate_order_total(order.id)

    @classmethod
    def calculate_order_total(cls, order_id):
        order = OrderRepository.get_order(order_id)
        
        subtotal = Decimal('0')
        for item in order.items:
            subtotal += Decimal(str(item['unit_price'])) * item['quantity']
        for combo in order.combos:
            subtotal += Decimal(str(combo['unit_price'])) * combo['quantity']
        
        tax = subtotal * cls.TAX_RATE
        total = subtotal + tax
        
        order.subtotal = subtotal
        order.tax = tax
        order.total_price = total
        order.save()
        
        return order

    @classmethod
    def apply_promotions(cls, order_id, promotion_codes):
        order = OrderRepository.get_order(order_id)
        for code in promotion_codes:
            promotion = PromotionService.get_valid_promotion(code)
            if promotion:
                OrderRepository.apply_promotion(order_id, promotion)
        return cls.calculate_order_total(order_id)

    @classmethod
    def update_order_status(cls, order_id, new_status):
        return OrderRepository.update_order_status(order_id, new_status)