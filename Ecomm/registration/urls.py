
from .views import *
from django.urls import path

urlpatterns = [
    path('register/', RegistrationView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),

    path('api/addresses/', AddressList.as_view(), name='address-list'),
    path('api/update_delivery_time/', update_delivery_time, name='update_delivery_time'),
    path('api/profile/', ProfileAPI.as_view(), name='profile'),

]
