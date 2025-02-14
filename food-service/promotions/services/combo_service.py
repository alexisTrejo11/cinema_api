from decimal import Decimal
from ..repository.combo_repository import ComboRepository

class ComboService:
    @classmethod
    def calculate_combo_savings(cls, combo_id):
        combo = ComboRepository.get_combo_by_id(combo_id)
        regular_price = sum(
            product.product.price * product.quantity
            for product in combo.comboproduct_set.all()
        )
        return regular_price - combo.price

    @classmethod
    def create_combo(cls, name, description, price, products):
        combo_data = {
            'name': name,
            'description': description,
            'price': price,
            'is_active': True
        }
        return ComboRepository.create_combo(combo_data, products)

    @classmethod
    def toggle_combo_status(cls, combo_id, is_active):
        return ComboRepository.update_combo_status(combo_id, is_active)