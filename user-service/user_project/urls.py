from django.contrib import admin
from django.urls import path, include
from accounts.views.auth_views import signup, LoginView, logout, LoginSuccessView
from accounts.views.user_views import UserViewSet
from wallet.views import WalletViewSet
from rest_framework.routers import DefaultRouter
from accounts.adapters import login_redirect
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView


router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'wallet', WalletViewSet, basename='wallet')

urlpatterns = [
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    path('admin/', admin.site.urls),
    path('signup/', signup, name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', logout, name='logout'),

   path('accounts/', include('allauth.urls')),
   path('api/auth/tokens/', login_redirect, name='login_redirect'),

   path('', include(router.urls)),

]