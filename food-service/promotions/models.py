from django.db import models
from products.models import Product

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
