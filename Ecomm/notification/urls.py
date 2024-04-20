from django.urls import path
from .views import SendNotificationAPI

urlpatterns = [
    path('send-notification/', SendNotificationAPI.as_view(), name='send_notification'),
]
