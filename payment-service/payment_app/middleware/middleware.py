from django.utils.deprecation import MiddlewareMixin
import time

class PaymentTrackingMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request.start_time = time.time()
    
    def process_response(self, request, response):
        if hasattr(request, 'start_time'):
            duration = time.time() - request.start_time
            response['X-Payment-Processing-Time'] = str(duration)
        return response