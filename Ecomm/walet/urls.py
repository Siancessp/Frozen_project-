from django.urls import path
from .views import *
urlpatterns = [
    path('api/wallet/', WalletAPIView.as_view(), name='wallet_api'),
    path('api/save_wallet_transaction/', save_and_update_wallet, name='save_wallet_transaction'),

    # Other URL patterns...
]
