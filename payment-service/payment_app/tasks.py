from celery import shared_task
from decimal import Decimal
from django.db.models import Sum, Count, Avg
from django.db import transaction
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

@shared_task(
    name='payment_app.tasks.generate_sales_report',
    bind=True,
    max_retries=3,
    default_retry_delay=60  # 1 minuto entre reintentos
)
def generate_sales_report(self, report_id):
    """
    Tarea asíncrona para generar reportes de ventas
    
    Args:
        report_id: ID del reporte a generar
    """
    from .models import SalesReport, Payment  # Importación local para evitar circular imports
    
    logger.info(f"Starting sales report generation for report_id: {report_id}")
    
    try:
        with transaction.atomic():
            report = SalesReport.objects.select_for_update().get(id=report_id)
            
            if report.status != 'generating':
                logger.warning(f"Report {report_id} is not in generating status")
                return
            
            # Obtener pagos completados en el rango de fechas
            payments = Payment.objects.filter(
                created_at__range=(report.start_date, report.end_date),
                status='completed'
            )
            
            # Calcular estadísticas básicas
            if payments.exists():
                payment_stats = payments.aggregate(
                    total_sales=Sum('amount'),
                    total_orders=Count('id'),
                    avg_order_value=Avg('amount'),
                    total_refunds=Sum('refund_amount')
                )
                
                total_sales = payment_stats.get('total_sales', Decimal('0.00'))
                total_orders = payment_stats.get('total_orders', 0)
                avg_order_value = payment_stats.get('avg_order_value', Decimal('0.00'))
                total_refunds = payment_stats.get('total_refunds', Decimal('0.00'))
            else:
                total_sales = Decimal('0.00')
                total_orders = 0
                avg_order_value = Decimal('0.00')
                total_refunds = Decimal('0.00')
            
            # Desglose por método de pago
            payment_method_stats = payments.values(
                'payment_method__name'
            ).annotate(
                total=Sum('amount'),
                count=Count('id')
            )
            
            """
            # Desglose por película si hay booking_id
            movie_stats = payments.exclude(
                booking_id__isnull=True
            ).values(
                'booking__movie__title'
            ).annotate(
                total=Sum('amount'),
                tickets=Count('booking__tickets')
            )
            
            # Desglose por horario de función
            showtime_stats = payments.exclude(
                booking_id__isnull=True
            ).values(
                'booking__showtime__start_time__hour'
            ).annotate(
                total=Sum('amount'),
                count=Count('id')
            )
            """
            
            # Actualizar el reporte con las estadísticas
            report.total_sales = total_sales
            report.total_orders = total_orders
            report.average_order_value = avg_order_value
            report.total_refunds = total_refunds
            report.net_sales = report.total_sales - report.total_refunds
            
            # Calcular ganancia bruta (asumiendo un margen del 60%)
            report.gross_profit = report.net_sales * Decimal('0.60')
            
            # Almacenar desgloses detallados
            report.payment_method_breakdown = {
                item['payment_method__name']: {
                    'total': str(item['total']),
                    'count': item['count']
                } for item in payment_method_stats
            }
            
            """
            report.movie_breakdown = {
                item['booking__movie__title']: {
                    'total': str(item['total']),
                    'tickets': item['tickets']
                } for item in movie_stats
            }
            
            report.showtime_breakdown = {
                f"{item['booking__showtime__start_time__hour']:02d}:00": {
                    'total': str(item['total']),
                    'count': item['count']
                } for item in showtime_stats
            }
            """
            
            report.status = 'completed'
            report.save()
            
            logger.info(f"Successfully generated sales report {report_id}")

            
    except SalesReport.DoesNotExist:
        logger.error(f"Report {report_id} not found")
        raise
        
    except Exception as e:
        logger.error(f"Error generating report {report_id}: {str(e)}")
        report.status = 'failed'
        report.save()
        
        # Reintenta la tarea si no se han agotado los reintentos
        if self.request.retries < self.max_retries:
            raise self.retry(exc=e)
        raise