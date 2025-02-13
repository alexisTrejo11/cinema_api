from django.db import models
import uuid
from decimal import Decimal
from promotions.models import Promotion

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('payment_pending', 'Payment Pending'),
        ('paid', 'Paid'),
        ('preparing', 'Preparing'),
        ('ready', 'Ready for Pickup'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    user_id = models.IntegerField()
    items = models.JSONField()  # Format: [{"product_id": "uuid", "quantity": 2, "unit_price": "10.00"}]
    combos = models.JSONField(default=list)  # Format: [{"combo_id": "uuid", "quantity": 1, "unit_price": "20.00"}]
    subtotal = models.DecimalField(max_digits=8, decimal_places=2)
    tax = models.DecimalField(max_digits=8, decimal_places=2)
    total_price = models.DecimalField(max_digits=8, decimal_places=2)
    applied_promotions = models.ManyToManyField(Promotion, through='OrderPromotion')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def calculate_total(self):
        self.subtotal = Decimal('0')
        for item in self.items:
            self.subtotal += Decimal(str(item['unit_price'])) * item['quantity']
        for combo in self.combos:
            self.subtotal += Decimal(str(combo['unit_price'])) * combo['quantity']
        self.tax = self.subtotal * Decimal('0.15')  # 15% tax
        self.total_price = self.subtotal + self.tax
        return self.total_price

    def __str__(self):
        return f"Order {self.id}"

class OrderPromotion(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    promotion = models.ForeignKey(Promotion, on_delete=models.CASCADE)
    discount_amount = models.DecimalField(max_digits=8, decimal_places=2)
    
    def __str__(self):
        return f"{self.promotion.name} applied to Order {self.order.id}"
