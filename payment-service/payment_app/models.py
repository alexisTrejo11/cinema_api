from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal
import uuid

class PaymentMethod(models.Model):
    """Model to store payment method configurations"""
    name = models.CharField(max_length=50, unique=True)
    is_active = models.BooleanField(default=True)
    configuration = models.JSONField(default=dict)  # Storing API keys, credentials, etc.
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Payment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
        ('partially_refunded', 'Partially Refunded'),
        ('cancelled', 'Cancelled'),
    ]
    
    reference_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user_id = models.IntegerField(db_index=True, null=True)
    booking_id = models.IntegerField(null=True, db_index=True)
    order_id = models.IntegerField(null=True, db_index=True)
    amount = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='pending',
        db_index=True
    )
    payment_method = models.ForeignKey(
        PaymentMethod,
        on_delete=models.PROTECT,
        related_name='payments'
    )
    transaction_id = models.CharField(max_length=100, blank=True, db_index=True)
    payment_details = models.JSONField(default=dict)  # Store payment gateway response
    error_message = models.TextField(blank=True)
    refund_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00')
    )
    ip_address = models.GenericIPAddressField(null=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['status', 'created_at']),
            models.Index(fields=['user_id', 'status']),
        ]

    def __str__(self):
        return f"Payment {self.reference_id}"

class PaymentRefund(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processed', 'Processed'),
        ('failed', 'Failed'),
    ]
    
    payment = models.ForeignKey(
        Payment,
        on_delete=models.PROTECT,
        related_name='refunds'
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    reason = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    refund_transaction_id = models.CharField(max_length=100, blank=True)
    processed_by = models.IntegerField()  # ID of staff user who processed the refund
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Refund {self.id} for Payment {self.payment.reference_id}"

class SalesReport(models.Model):
    REPORT_TYPE_CHOICES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('custom', 'Custom'),
    ]
    
    reference_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    report_type = models.CharField(max_length=20, choices=REPORT_TYPE_CHOICES)
    total_sales = models.DecimalField(max_digits=12, decimal_places=2)
    total_orders = models.IntegerField()
    total_items_sold = models.IntegerField()
    average_order_value = models.DecimalField(max_digits=10, decimal_places=2)
    total_discounts = models.DecimalField(max_digits=12, decimal_places=2)
    total_refunds = models.DecimalField(max_digits=12, decimal_places=2)
    net_sales = models.DecimalField(max_digits=12, decimal_places=2)
    gross_profit = models.DecimalField(max_digits=12, decimal_places=2)
    payment_method_breakdown = models.JSONField(default=dict)
    movie_breakdown = models.JSONField(default=dict)
    showtime_breakdown = models.JSONField(default=dict)
    status = models.CharField(
        max_length=20,
        choices=[
            ('generating', 'Generating'),
            ('completed', 'Completed'),
            ('failed', 'Failed'),
        ],
        default='generating'
    )
    generated_by = models.IntegerField(null=True)  # ID of user who generated the report
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['report_type', 'start_date']),
            models.Index(fields=['status', 'created_at']),
        ]

    def __str__(self):
        return f"{self.report_type} Sales Report ({self.reference_id})"
