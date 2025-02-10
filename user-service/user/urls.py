from django.contrib import admin
from django.urls import path
from accounts.views import signup, LoginView, logout
from wallet.views import get_wallet_info, add_credit, make_purchase

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/', signup, name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', logout, name='logout'),

    path('wallet/', get_wallet_info, name='get_wallet_info'),
    path('wallet/add-credit/', add_credit, name='add_credit'),
    path('wallet/make-purchase/', make_purchase, name='make_purchase'),
]

