from django.urls import path, include
from rest_framework.routers import DefaultRouter
from food_orders.views import ProductViewSet, OrderViewSet
from django.contrib import admin

router = DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'orders', OrderViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/', include('food.urls')),

]
