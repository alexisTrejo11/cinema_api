from django.db import models

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
