from django.db.models import Q
from django.shortcuts import render, redirect

# Create your views here.
from django.shortcuts import get_object_or_404, render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from .models import  Order
from .serializers import OrderSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from ecomApp.models import CustomUser
from ecomApp.models import Catagory
from ecomApp.models import Product
#for noww...
class OrderView(APIView):
    def post(self, request):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class OrderList(APIView):
#     def get(self, request, pk):
#         user = get_object_or_404(Order, pk=pk)
#         serializer = OrderSerializer(user)
#         return Response(serializer.data)
#
#     def put(self, request, pk):
#         user = get_object_or_404(Order, pk=pk)
#         serializer = OrderSerializer(user, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def delete(self, request, pk):
#         user = get_object_or_404(Order, pk=pk)
#         user.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
#for noww...


def orderlist(request):
    orderapp=Order.objects.all()

    context={
         'ordform': orderapp
     }
    return render(request,'backend/orderlist.html',context)
def confirmorderlist(request):
    ordercon=Order.objects.filter(Q(status=2) | Q(status=3) | Q(status=4))
    context={
        'ordercon':ordercon

    }
    return render(request,'backend/confirmorderlist.html',context)
def view_item(request, myid):
     sel_ordform = Order.objects.get(id=myid)
     ord = Order.objects.all()
     context = {
         'ordform': ord,
         'sel_ordform': sel_ordform
    }
     return render(request, 'backend/orderview.html', context)

# def activate_catagory(request, catagory_id):
#     banner = get_object_or_404(Order, id=catagory_id)
#     banner.status = 3
#     banner.save()
#     return redirect('orderapp')  # Redirect to your banner list view
#
# def deactivate_catagory(request, catagory_id):
#     banner = get_object_or_404(Order, id=catagory_id)
#     banner.status = 4
#     banner.save()
#     return redirect('orderapp')  # Redirect to your banner list view
# # Create your views here.
# def suspend_user(request, catagory_id):
#     banner = get_object_or_404(Order, id=catagory_id)
#     banner.status = 2
#     banner.save()
#
#
#     return redirect('orderapp')  # Redirect to your category list view
# def returnrequest(request, catagory_id):
#     banner = get_object_or_404(Order, id=catagory_id)
#     banner.status = 6
#     banner.save()
#
#
#     return redirect('orderapp')
# def returnaccepted(request, catagory_id):
#     banner = get_object_or_404(Order, id=catagory_id)
#     banner.status = 7
#     banner.save()
#
#
#     return redirect('orderapp')
# def deliver(request, catagory_id):
#     banner = get_object_or_404(Order, id=catagory_id)
#     banner.status = 5
#     banner.save()
#
#
#     return redirect('orderapp')  # Redirect to your category list view
# def cancel(request, catagory_id):
#     banner = get_object_or_404(Order, id=catagory_id)
#     banner.status = 1
#     banner.save()
#
#
#     return redirect('orderapp')  # Redirect to your category list view





def suspend_user(request, catagory_id):
    banner = get_object_or_404(Order, id=catagory_id)
    banner.status = 2
    banner.save()
    return redirect('activate_catagory', catagory_id=catagory_id)

def activate_catagory(request, catagory_id):
    banner = get_object_or_404(Order, id=catagory_id)
    banner.status = 3
    banner.save()
    return redirect('deactivate_catagory', catagory_id=catagory_id)

def deactivate_catagory(request, catagory_id):
    banner = get_object_or_404(Order, id=catagory_id)
    banner.status = 4
    banner.save()
    return redirect('deliver', catagory_id=catagory_id)

def deliver(request, catagory_id):
    banner = get_object_or_404(Order, id=catagory_id)
    banner.status = 5
    banner.save()
    return redirect('cancel', catagory_id=catagory_id)

def cancel(request, catagory_id):
    banner = get_object_or_404(Order, id=catagory_id)
    banner.status = 1
    banner.save()
    return redirect('', catagory_id=catagory_id)

# def returnrequest(request, catagory_id):
#     banner = get_object_or_404(Order, id=catagory_id)
#     banner.status = 6
#     banner.save()
#     return redirect('returnaccepted', catagory_id=catagory_id)
#
# def returnaccepted(request, catagory_id):
#     banner = get_object_or_404(Order, id=catagory_id)
#     banner.status = 7
#     banner.save()
#     return redirect('orderapp')  # Redirect to your category list view
#











import random
import string

def generate_random_order_id():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
import secrets
@api_view(['POST'])
def create_order(request):
    # Assuming the user ID is sent in the request data
    user_id = request.data.get('user')
    pay = request.data.get('payment_id')
    cou = request.data.get('coupon',"df                                         ")

    user = get_object_or_404(CustomUser, id=user_id)
    cart_items = Cartapi.objects.filter(user_id=user)

    # Generate a random alphanumeric order_id with a prefix
    order_id_prefix = 'gain_'
    random_part = secrets.token_hex(8)  # Adjust the length of the token as needed
    order_id = f'{order_id_prefix}{random_part}'

    # Create orders from cart items
    for cart_item in cart_items:
        order_data = {
            'order_id': order_id,
            'user_id': user.id,
            'cat_id': cart_item.product_id.cat_name.id,
            'product_id': cart_item.product_id.id,
            'quantity': cart_item.quantity,
            'payment_id': pay,
            'couponcode': cou,
            'amount': cart_item.total_price,
            'status': 1,  # Set your status accordingly
        }

        order_serializer = OrderSerializer(data=order_data)
        if order_serializer.is_valid():
            order_serializer.save()
        else:
            return JsonResponse({'error': order_serializer.errors}, status=400)

    # Delete all cart items for the user
    cart_items.delete()

    return JsonResponse({'message': 'Orders created successfully'})

from django.contrib import messages
def update_status(request, order_id):
    if request.method == 'POST':
        selected_status = request.POST.get('status')
        order = Order.objects.get(id=order_id)
        order.status = selected_status
        order.save()
        messages.success(request, 'Status updated successfully!')

    return redirect(request.META.get('HTTP_REFERER', 'fallback_url')) # Replace with your actual redirect URL

