from django.db.models import Q
from django.shortcuts import render, redirect
from cart.models import CartCoupon
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


def orderlist(request):
    # Fetch all orders
    orders = Order.objects.all()

    # Create a dictionary to store orders grouped by their order_id
    orders_dict = {}

    # Iterate over orders and group them by their order_id
    for order in orders:
        if order.payment_id:
            if order.order_id not in orders_dict:
                orders_dict[order.order_id] = order
    # Extract the first element of each group
    first_elements = [order for order in orders_dict.values()]

    # Pass the first elements to the template context
    context = {
        'ordform': first_elements
    }

    return render(request, 'backend/orderlist.html', context)

def confirmorderlist(request):
    ordercon=Order.objects.filter(Q(status=2) | Q(status=3) | Q(status=4))
    context={
        'ordercon':ordercon

    }
    return render(request,'backend/confirmorderlist.html',context)
def view_item(request, myid):
     sel_ordform = Order.objects.filter(order_id=myid)
     ord = Order.objects.all()
     print(sel_ordform)
     # related_orders = Order.objects.filter(order_id=sel_ordform.order_id)
     context = {
         'ordform': ord,
         'sel_ordform': sel_ordform
    }
     return render(request, 'backend/orderview.html', context)




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

from django.contrib import messages
import razorpay
from django.conf import settings
from django.http import JsonResponse, HttpResponseServerError
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist

from decimal import Decimal
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes


def update_status(request, id):
    if request.method == 'POST':
        selected_status_str = request.POST.get('selected_status')
        try:
            selected_status = int(selected_status_str)
        except (TypeError, ValueError):
            # Handle the case where selected_status_str is not a valid integer
            messages.error(request, 'Invalid status value!')
            return redirect(request.META.get('HTTP_REFERER', 'fallback_url'))

        order = Order.objects.get(id=id)
        order.status = selected_status

        # Convert amount, price, and total_price to Decimal

        order.save()
        messages.success(request, 'Status updated successfully!')

    return redirect(request.META.get('HTTP_REFERER', 'fallback_url'))  # Replace with your actual redirect URL


razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_SECRET_KEY))
@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_order(request):
    if request.method == 'POST':
        user_id = request.data.get('user_id')
        total_amount = request.data.get('total_amount')
        dicounted_price = request.data.get('dicounted_price')
        previous_price = request.data.get('previous_price')
        delivery_price = request.data.get('delivery_price')

        coupon_code = request.data.get('coupon_code')
        coupon_value = request.data.get('coupon_value')
        newname = request.data.get('newname', "")
        phone = request.data.get('phone', "")
        address = request.data.get('address', "Pick UP")
        city = request.data.get('city', "")
        state = request.data.get('state', "")
        country = request.data.get('country', "")
        zip_code = request.data.get('zip_code', "")
        delivery_time = request.data.get('delivery_time', "")
        try:
            print(user_id)
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
                    status=1,  # Set initial status
                    quantity=cart_item.quantity,
                    price=cart_item.price,
                    total_price=total_amount,
                    previous_price=previous_price,
                    dicounted_price=dicounted_price,
                    delivery_price=delivery_price,
                    signature='',  # Leave signature empty initially
                    newname=newname,
                    phone=phone,
                    address=address,
                    city=city,
                    state=state,
                    country=country,
                    zip_code=zip_code,
                    delivery_time=delivery_time,

                )
            cart_items.delete()
            cart_coupon = CartCoupon.objects.filter(user_id=user_id)
            if cart_coupon:
                cart_coupon.delete()
            return JsonResponse({'razorpay_order_id': razorpay_order['id'], 'couponcode': coupon_code, 'total_price': total_amount,'status':'success'}, status=200)
        except ObjectDoesNotExist:
            return JsonResponse({'error': 'User does not exist'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return HttpResponseServerError("Method Not Allowed")
from uuid import uuid4  # Import UUID generator

@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def verify_payment(request):
    if request.method == 'POST':
        try:
            razorpay_payment_id = request.data.get('razorpay_payment_id')
            razorpay_order_id = request.data.get('razorpay_order_id')
            razorpay_signature = request.data.get('razorpay_signature')

            # Verify payment signature
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': razorpay_payment_id,
                'razorpay_signature': razorpay_signature
            }
            razorpay_client.utility.verify_payment_signature(params_dict)

            # Update order status or save payment details to your database
            orders = Order.objects.filter(order_id=razorpay_order_id)
            for order in orders:
                # Generate a unique order item ID
                order_item_id = str(uuid4())
                order.payment_id = razorpay_payment_id
                order.signature = razorpay_signature
                order.status = 1  # Set status to success
                order.order_item_id = order_item_id
                order.save()

            return JsonResponse({'message': 'Payment successful'}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
        else:
            return HttpResponseServerError("Method Not Allowed")
from rest_framework import generics
from rest_framework.response import Response
from .models import Order
from .serializers import GroupedOrderSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Order
from .serializers import OrderSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Order
from .serializers import OrderSerializer


class OrderListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_id = request.query_params.get('user_id')

        # Fetch all orders for the given user
        orders = Order.objects.filter(user_id=user_id)

        # Extract unique tuples containing order_id, created_at, total_price, and status
        unique_orders = set((order.order_id, order.created_at, order.total_price, order.status) for order in orders)

        # Construct list of dictionaries for each unique order
        order_list = []
        for order in unique_orders:
            order_dict = {
                'order_id': order[0],
                'created_at': order[1].strftime("%d %b %Y, %I:%M %p"),
                'total_price': order[2],
                'status': order[3]
            }
            order_list.append(order_dict)

        # Sort the order list in descending order based on created_at
        sorted_order_list = sorted(order_list, key=lambda x: x['created_at'], reverse=True)

        return Response(sorted_order_list)
from datetime import date
from rest_framework import serializers
from .models import CustomUser

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'


class OrderDetailsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            # Get the order_id from query parameters
            order_id = request.query_params.get('order_id')

            # Check if order_id parameter is provided
            if order_id is None:
                return Response({"error": "order_id parameter is required"}, status=status.HTTP_400_BAD_REQUEST)

            # Retrieve all orders for the specified order_id
            orders = Order.objects.filter(order_id=order_id)

            # If no orders found for the given order_id
            if not orders:
                return Response({"error": "No orders found for the given order_id"}, status=status.HTTP_404_NOT_FOUND)

            # Initialize lists to store product details and order details
            products = []
            order_details = []

            # Iterate over orders
            for order in orders:
                # Retrieve product details for all orders
                product = {
                    "product_id": order.product_id.id,
                    "name": order.product_id.title,
                    "description": order.product_id.description,
                    "item_photo": order.product_id.item_photo.url,
                    "item_quantity": order.quantity,
                    "item_measurement": order.product_id.item_measurement,
                    "item_old_price": order.product_id.item_old_price,
                    "discount": order.product_id.discount,
                    "item_new_price": order.product_id.item_new_price,
                    "product_order_price":order.product_id.item_new_price*order.quantity,
                    "status": order.product_id.status,
                    "category": order.product_id.category.name,
                    "created_at": order.product_id.created_at,
                    "deal_of_the_day": order.product_id.deal_of_the_day,
                    "recommended": order.product_id.recommended,
                    "most_popular": order.product_id.most_popular
                }
                products.append(product)

                # Append full order details for the first order only
                if not order_details:  # Ensures only the first order details are added
                    order_detail = {
                        "order_id": order.order_id,
                        "status": order.status,
                        "total_price": order.total_price,
                        "discounted_price": order.dicounted_price,
                        "previous_price": order.previous_price,
                        "delivery_price":order.delivery_price,
                        "coupon_code":order.couponcode,
                        # "item_price": order.price,
                        # "created_at": order.created_at,
                        "newname": order.newname,
                        "phone": order.phone,
                        "address": order.address,
                        "city": order.city,
                        "state": order.state,
                        "country": order.country,
                        "zip_code": order.zip_code,
                        "delivery_time": order.delivery_time,
                        # "order_item_id": order.order_item_id
                    }
                    order_details.append(order_detail)

            return Response({"order_details": order_details, "products": products}, status=status.HTTP_200_OK)



        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)