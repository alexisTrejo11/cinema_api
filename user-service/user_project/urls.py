from django.contrib import admin
from django.urls import path, include
from accounts.views.auth_views import signup, LoginView, logout, LoginSuccessView
from accounts.views.user_views import UserViewSet
from wallet.views import WalletViewSet
from rest_framework.routers import DefaultRouter
from accounts.adapters import login_redirect

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'wallet', WalletViewSet, basename='wallet')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/', signup, name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', logout, name='logout'),

   path('accounts/', include('allauth.urls')),
   path('api/auth/tokens/', login_redirect, name='login_redirect'),


   path('', include(router.urls)),

]