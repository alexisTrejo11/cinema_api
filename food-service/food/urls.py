# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from food_orders import views

router = DefaultRouter()
router.register(r'products', views.ProductViewSet)
router.register(r'combos', views.ComboViewSet)
router.register(r'promotions', views.PromotionViewSet)
router.register(r'orders', views.OrderViewSet)

urlpatterns = [
    path('', include(router.urls)),
]