from ..services.report_service import ReportService
from ..models import SalesReport
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from ..serializers import ReportSerializer

class SalesReportViewSet(viewsets.ModelViewSet):
    queryset = SalesReport.objects.all()
    serializer_class = ReportSerializer

    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.report_service = ReportService()
    
    @action(detail=False, methods=['post'])
    def generate(self, request):
        try:
            report = self.report_service.create_report(
                start_date=request.data.get('start_date'),
                end_date=request.data.get('end_date'),
                report_type=request.data.get('report_type'),
                user_id=request.user.id
            )
            
            return Response({
                'status': 'success',
                'report_id': report.reference_id
            })
            
        except Exception as e:
            return Response({
                'status': 'error',
                'message': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
