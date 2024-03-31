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
from cart.models import Cart
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
import razorpay
from django.conf import settings
from django.http import JsonResponse, HttpResponseServerError
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist

def update_status(request, order_id):
    if request.method == 'POST':
        selected_status = request.POST.get('status')
        order = Order.objects.get(id=order_id)
        order.status = selected_status
        order.save()
        messages.success(request, 'Status updated successfully!')

    return redirect(request.META.get('HTTP_REFERER', 'fallback_url')) # Replace with your actual redirect URL

razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_SECRET_KEY))
@csrf_exempt
@api_view(['POST'])
def create_order(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        total_amount = request.POST.get('total_amount')
        coupon_code = request.POST.get('coupon_code')
        coupon_value = request.POST.get('coupon_value')

        try:
            # Create order in Razorpay
            order_amount = int(float(total_amount) * 100)  # Amount in paisa
            order_currency = 'INR'
            order_receipt = 'order_receipt_' + str(user_id)  # You can set it as per your requirement
            razorpay_order = razorpay_client.order.create(dict(amount=order_amount, currency=order_currency, receipt=order_receipt))

            # Get cart items for the user
            cart_items = Cart.objects.filter(u_id=user_id, status='Active')

            # Create orders for each item in the cart
            for cart_item in cart_items:
                Order.objects.create(
                    order_id=razorpay_order['id'],
                    user_id=CustomUser.objects.get(id=user_id),
                    product_id=cart_item.product_id,
                    payment_id='',  # Leave payment_id empty initially
                    couponcode=coupon_code,
                    amount=cart_item.price,
                    status=0,  # Set initial status
                    quantity=cart_item.quantity,
                    price=cart_item.price,
                    total_price=total_amount,
                    signature='',  # Leave signature empty initially
                )

            return JsonResponse({'razorpay_order_id': razorpay_order['id'], 'couponcode': coupon_code, 'total_price': total_amount}, status=200)
        except ObjectDoesNotExist:
            return JsonResponse({'error': 'User does not exist'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return HttpResponseServerError("Method Not Allowed")

@csrf_exempt
@api_view(['POST'])
def verify_payment(request):
    if request.method == 'POST':
        try:
            razorpay_payment_id = request.POST.get('razorpay_payment_id')
            razorpay_order_id = request.POST.get('razorpay_order_id')
            razorpay_signature = request.POST.get('razorpay_signature')

            # Verify payment signature
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': razorpay_payment_id,
                'razorpay_signature': razorpay_signature
            }
            razorpay_client.utility.verify_payment_signature(params_dict)

            # Update order status or save payment details to your database
            order = Order.objects.get(order_id=razorpay_order_id)
            order.payment_id = razorpay_payment_id
            order.signature = razorpay_signature
            order.status = 1  # Set status to success
            order.save()

            return JsonResponse({'message': 'Payment successful'}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return HttpResponseServerError("Method Not Allowed")