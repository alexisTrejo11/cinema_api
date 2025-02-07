from celery import shared_task
from datetime import datetime, timedelta
from decimal import Decimal
from django.db.models import Sum, Avg, Count
from django.db import transaction
from ..models import SalesReport, Payment
import logging

logger = logging.getLogger(__name__)

@shared_task
def generate_sales_report(report_id):
    
    try:
        report = SalesReport.objects.get(id=report_id)
        
        with transaction.atomic():
            # Calcular estadísticas básicas
            payments = Payment.objects.filter(
                created_at__range=(report.start_date, report.end_date),
                status='completed'
            )
            
            stats = payments.aggregate(
                total_sales=Sum('amount'),
                total_orders=Count('id'),
                avg_order=Avg('amount'),
                total_refunds=Sum('refund_amount')
            )
            
            # Desglose por método de pago
            payment_method_stats = payments.values('payment_method__name').annotate(
                total=Sum('amount'),
                count=Count('id')
            )
            
            # Desglose por película
            movie_stats = payments.values('booking__movie__title').annotate(
                total=Sum('amount'),
                tickets=Count('booking__tickets')
            )
            
            # Actualizar reporte
            report.total_sales = stats['total_sales'] or Decimal('0')
            report.total_orders = stats['total_orders'] or 0
            report.average_order_value = stats['avg_order'] or Decimal('0')
            report.total_refunds = stats['total_refunds'] or Decimal('0')
            report.net_sales = report.total_sales - report.total_refunds
            
            report.payment_method_breakdown = {
                item['payment_method__name']: {
                    'total': str(item['total']),
                    'count': item['count']
                } for item in payment_method_stats
            }
            
            report.movie_breakdown = {
                item['booking__movie__title']: {
                    'total': str(item['total']),
                    'tickets': item['tickets']
                } for item in movie_stats
            }
            
            report.status = 'completed'
            report.save()
            
    except Exception as e:
        logger.error(f"Error generating report {report_id}: {str(e)}")
        report.status = 'failed'
        report.save()