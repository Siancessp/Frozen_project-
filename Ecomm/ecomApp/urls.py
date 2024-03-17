from .views import *
from django.urls import path

urlpatterns = [

    path('backend/dashboard', dashboard , name="backend/dashboard"),
    path('backend/charts', charts , name="backend/charts"),
    path('backend/verify-email/', verify_email, name='backend/verify_email'),
    path('backend/verify-otp/', verify_otp, name='verify_otp'),
    path('backend/change-password/', change_password, name='change_password'),

    # path('backend/userlist/share_income/<int:myid>/', share_income, name='userlist/share_income'),
     path('backend/catagoryapp/', catagory, name="catagoryapp"),
     path('backend/catgoryadd/', catgoryadd, name="catgoryadd"),
     path('backend/catagoryapp/delete_item/<int:myid>/', delete_item, name="catagory/delete_item"),
     path('backend/catagoryapp/edit_item/<int:myid>/', edit_item, name="catagory/edit_item"),
     path('backend/catagoryapp/update_item/<int:myid>/', update_item, name="catagory/update_item"),
     path('backend/catagoryapp/view_item/<int:myid>/', view_item, name="catagory/view_item"),
     path('backend/catagoryapp/activate_catagory/<int:catagory_id>/', activate_catagory, name='catgoryapp/activate_catagory'),
     path('backend/catagoryapp/deactivate_catagory/<int:catagory_id>/', deactivate_catagory, name='catgoryapp/deactivate_catagory'),


    path('backend/productapp/', product, name="productapp"),
     path('backend/productadd/', productadd, name="productadd"),
     path('backend/productapp/delete_item/<int:myid>/', delete_product, name="delete_item"),
     path('backend/productapp/edit_item/<int:myid>/', edit_product, name="edit_item"),
     path('backend/productapp/update_item/<int:myid>/', update_product, name="update_item"),
     path('backend/productapp/view_item/<int:myid>/', view_product, name="view_item"),
     path('backend/productapp/activate_product/<int:product_id>/', activate_product, name='productapp/activate_product'),
     path('backend/productapp/deactivate_product/<int:product_id>/', deactivate_product, name='productapp/deactivate_product'),


    path('backend/customerlist/', customerlist, name="customerlist"),
    path('backend/customerlist/activate_product/<int:id>/', activate_customer, name='customerlist/activate_customer'),
    path('backend/customerlist/deactivate_product/<int:id>/', deactivate_customer,name='customerlist/deactivate_customer'),

    path('backend/customer_couponlist/', customer_couponlist, name='customer_couponlist'),
    path('backend/customer_couponlist/add_customer_coupon/', add_customer_coupon, name='add_customer_coupon'),
    path('backend/customer_couponlist/delete_item/<int:coupon_id>/', delete_coupon, name="customer_couponlist/delete_item"),
    path('backend/customer_couponlist/activate_coupon/<int:coupon_id>/', activate_coupon, name='customer_couponlist/activate_coupon'),
    path('backend/customer_couponlist/deactivate_coupon/<int:coupon_id>/', deactivate_coupon,
         name='customer_couponlist/deactivate_coupon'),

]
