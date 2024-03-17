# views.py
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from django_otp import devices_for_user
from django_otp.plugins.otp_static.models import StaticDevice
# from .serializers import RegistrationSerializer
from ecomApp.models import CustomUser
import random
# views.py
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django_otp import devices_for_user
from django_otp.plugins.otp_static.models import StaticDevice

from ecomApp.models import Otp
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
User = get_user_model()
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer
#
# @api_view(['POST'])
# def register_with_mobile(request):
#     if request.method == 'POST':
#         phone_number = request.POST.get('phone_number')
#
#         # Check if the phone number already exists
#         if User.objects.filter(phone_number=phone_number).exists():
#             return JsonResponse({'error': 'Phone number already registered'}, status=400)
#
#         # Generate OTP
#         otp_code = ''.join([str(random.randint(0, 9)) for _ in range(6)])  # Generate a random 6-digit OTP
#         user = User.objects.create_user(phone_number=phone_number)
#         Otp.objects.create(user=user, otp_code=otp_code)
#
#         # Send OTP to the user (you'll implement this part)
#         # For example, you can use SMS or any other communication method
#
#         return JsonResponse({'message': 'OTP sent successfully'}, status=200)
#
#     return JsonResponse({'error': 'Invalid request method'}, status=405)
#
#
# # views.py continued...
# from django.utils import timezone
#
# @api_view(['POST'])
# def verify_otp(request):
#     if request.method == 'POST':
#         phone_number = request.POST.get('phone_number')
#         otp_code = request.POST.get('otp_code')
#
#         user = CustomUser.objects.filter(phone_number=phone_number).first()
#         if not user:
#             return JsonResponse({'error': 'User not found'}, status=404)
#
#         otp = Otp.objects.filter(user=user, otp_code=otp_code).first()
#         if not otp:
#             return JsonResponse({'error': 'Invalid OTP'}, status=400)
#
#         # Check if OTP is expired (e.g., within 5 minutes)
#         if timezone.now() - otp.created_at > timezone.timedelta(minutes=5):
#             return JsonResponse({'error': 'OTP expired'}, status=400)
#
#         # Delete OTP after successful verification
#         otp.delete()
#
#         # Create device for user (you may customize this according to your needs)
#         StaticDevice.objects.create(user=user)
#
#         return JsonResponse({'message': 'OTP verified successfully'}, status=200)
#
#     return JsonResponse({'error': 'Invalid request method'}, status=405)
#
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password
@api_view(['POST'])
def register_user(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        try:
            if serializer.is_valid():
                # Hash the password before saving
                password = make_password(serializer.validated_data.get('password'))
                serializer.validated_data['password'] = password
                user = serializer.save()
                return Response({"message": "Registration successful!"}, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except CustomUser.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
@api_view(['POST'])
def login_user(request):
    if request.method == 'POST':
        phone_number = request.data.get('phone_number')
        password = request.data.get('password')
        try:
            user = CustomUser.objects.get(phone_number=phone_number)
        except CustomUser.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        if check_password(password, user.password):
            return Response({"message": "Login successful!","user_id":user.id,"status":"success"}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)