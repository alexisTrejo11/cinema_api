from ..models import SalesReport
from django.core.exceptions import ValidationError
from datetime import datetime
from ..tasks import generate_sales_report

class ReportService:
    def create_report(self, start_date, end_date, report_type, user_id):
        """Create and initialize sales report"""
        self._validate_report_params(start_date, end_date, report_type)

        report = SalesReport.objects.create(
        start_date=start_date,
        end_date=end_date,
        report_type=report_type,
        total_sales=0.00,
        total_orders=0,
        total_items_sold=0,
        average_order_value=0.00,
        total_discounts=0.00,
        total_refunds=0.00,
        net_sales=0.00,
        gross_profit=0.00,
        payment_method_breakdown={},
        movie_breakdown={},
        showtime_breakdown={},
        generated_by=1
        )
        
        # Trigger async report generation
        generate_sales_report.delay(report.id)
        return report

    def _validate_report_params(self, start_date, end_date, report_type):
        if not all([start_date, end_date, report_type]):
            raise ValidationError('Missing required parameters')
            
        if start_date > end_date:
            raise ValidationError('Start date must be before end date')
            
        if report_type not in dict(SalesReport.REPORT_TYPE_CHOICES):
            raise ValidationError('Invalid report type')
