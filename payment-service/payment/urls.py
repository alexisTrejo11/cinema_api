from django.urls import path, include
from rest_framework.routers import DefaultRouter
from payment_app.views.payment_views import PaymentViewSet
from payment_app.views.report_views import SalesReportViewSet

router = DefaultRouter()
router.register(r'payments', PaymentViewSet, basename='payment')
router.register(r'reports', SalesReportViewSet, basename='report')

urlpatterns = [
    path('api/v1/', include(router.urls)),
]