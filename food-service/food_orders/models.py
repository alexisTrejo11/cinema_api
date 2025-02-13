from django.db import models
import uuid
from decimal import Decimal

class Product(models.Model):
    CATEGORY_CHOICES = [
        ('snacks', 'Snacks'),
        ('drinks', 'Drinks'),
        ('sweets', 'Sweets'),
        ('meals', 'Meals'),
        ('desserts', 'Desserts'),
        ('combo', 'Combos'),
    ]
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    image_url = models.URLField(blank=True, null=True)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    stock_quantity = models.IntegerField(default=0)
    cost_price = models.DecimalField(max_digits=6, decimal_places=2, help_text="Cost price for profit calculation")

    def __str__(self):
        return self.name

class Combo(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    products = models.ManyToManyField(Product, through='ComboProduct')
    price = models.DecimalField(max_digits=6, decimal_places=2)
    is_active = models.BooleanField(default=True)
    image_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def calculate_savings(self):
        regular_price = sum(product.price for product in self.products.all())
        return regular_price - self.price

    def __str__(self):
        return self.name

class ComboProduct(models.Model):
    combo = models.ForeignKey(Combo, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('combo', 'product')


class Promotion(models.Model):
    DISCOUNT_TYPE_CHOICES = [
        ('percentage', 'Percentage'),
        ('fixed', 'Fixed Amount'),
        ('bogo', 'Buy One Get One'),
    ]
    name = models.CharField(max_length=100)
    description = models.TextField()
    discount_type = models.CharField(max_length=20, choices=DISCOUNT_TYPE_CHOICES)
    discount_value = models.DecimalField(max_digits=5, decimal_places=2)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    products = models.ManyToManyField(Product, blank=True)
    combos = models.ManyToManyField(Combo, blank=True)
    min_purchase_amount = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    usage_limit = models.IntegerField(null=True, blank=True)
    current_usage = models.IntegerField(default=0)
    
    def is_valid(self):
        from django.utils import timezone
        now = timezone.now()
        return (self.start_date <= now <= self.end_date and
                (self.usage_limit is None or self.current_usage < self.usage_limit))

    def __str__(self):
        return self.name

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
