from django.urls import path

from .views import *

urlpatterns = [
    path('backend/orderapp/', orderlist, name="orderapp"),
    path('backend/confirmorderapp/', confirmorderlist, name="confirmorderapp"),
    path('backend/orderapp/view_item/<int:myid>/', view_item, name="orderapp/view_item"),
    # path('api/order/<int:pk>/', OrderList.as_view(), name='order-detail'),
    path('api/order/', OrderView.as_view(), name='user-order'),
    path('backend/orderapp/activate_catagory/<int:catagory_id>/', activate_catagory,name='orderapp/activate_catagory'),
    path('backend/orderapp/deactivate_catagory/<int:catagory_id>/', deactivate_catagory,name='orderapp/deactivate_catagory'),
    path('backend/orderapp/suspend_user/<int:catagory_id>/', suspend_user, name='orderapp/suspend_user'),
    path('backend/orderapp/deliver/<int:catagory_id>/', deliver, name='orderapp/deliver'),
    path('backend/orderapp/cancel/<int:catagory_id>/', cancel, name='orderapp/cancel'),
    # path('backend/orderapp/returnrequest/<int:catagory_id>/', returnrequest, name='orderapp/returnrequest'),
    # path('backend/orderapp/returnaccepted/<int:catagory_id>/', returnaccepted, name='orderapp/returnaccepted'),
    path('update_status/<int:order_id>/', update_status, name='update_status'),

    # path('api/create_order/', create_order, name='create_order')
    # ... other URLs
]
