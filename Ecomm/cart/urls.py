
from .views import *
from django.urls import path
from .views import *

urlpatterns = [
    path('api/add_to_cart/', AddToCartAPIView.as_view(), name='add_to_cart'),
    path('api/get_cart/', CartDetailsAPIView.as_view(), name='get_cart'),

    path('api/increase/', IncreaseQuantity.as_view(), name='increase'),
    path('api/decrease/', DecreaseQuantity.as_view(), name='decrease'),

    path('api/remove-cart-item/', RemoveCartItem.as_view(), name='remove_cart_item'),
    path('api/get_total_price/', CartTotalPrice.as_view(), name='CartTotalPrice'),

]