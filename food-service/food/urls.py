# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from products.views import ProductViewSet
from promotions.views import PromotionViewSet, ComboViewSet
from orders.views import OrderViewSet
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView


router = DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'combos', ComboViewSet)
router.register(r'promotions', PromotionViewSet)
router.register(r'orders', OrderViewSet)

urlpatterns = [
    path('', include(router.urls)),

    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]