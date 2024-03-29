# views.py
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
# from django_otp import devices_for_user
# from .serializers import RegistrationSerializer
from ecomApp.models import CustomUser
import random
# views.py
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from ecomApp.models import Otp
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
User = get_user_model()
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import CustomUserSerializer
from rest_framework_simplejwt.tokens import RefreshToken

# @api_view(['POST'])
# def register_user(request):
#     if request.method == 'POST':
#         serializer = UserSerializer(data=request.data)
#         try:
#             if serializer.is_valid():
#                 # Hash the password before saving
#                 password = make_password(serializer.validated_data.get('password'))
#                 serializer.validated_data['password'] = password
#                 user = serializer.save()
#                 return Response({"message": "Registration successful!"}, status=status.HTTP_201_CREATED)
#             else:
#                 return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#         except CustomUser.DoesNotExist:
#             return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
#         except Exception as e:
#             return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
# @api_view(['POST'])
# def login_user(request):
#     if request.method == 'POST':
#         phone_number = request.data.get('phone_number')
#         password = request.data.get('password')
#         try:
#             user = CustomUser.objects.get(phone_number=phone_number)
#         except CustomUser.DoesNotExist:
#             return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
#
#         if check_password(password, user.password):
#             return Response({"message": "Login successful!","user_id":user.id,"status":"success"}, status=status.HTTP_200_OK)
#         else:
#             # return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password

AUTH_USER_MODEL = 'ecomApp.CustomUser'



class RegistrationView(APIView):
    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)
        print(request.data, "============")
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)

            response_data = {
                'status':'success',
                'refresh': str(refresh)
,
                'access': str(refresh.access_token),
            }
            return Response(response_data, status=201)
        return Response(serializer.errors, status=400)



from rest_framework.permissions import AllowAny

class LoginView(APIView):
    permission_classes = [AllowAny]  # Allow access to all users

    def post(self, request):
        phone_number = request.data.get('phone_number')
        password = request.data.get('password')

        # Authenticate the user using the provided credentials
        user = authenticate(request, phone_number=phone_number, password=password)

        if user is not None:
            # Authentication successful, generate tokens
            refresh = RefreshToken.for_user(user)

            response_data = {
                'status': 'success',

                'refresh': str(refresh)
                ,
                'access': str(refresh.access_token),
            }
            return Response(response_data, status=200)
        else:
            # Authentication failed
            return Response({'error': 'Invalid credentials'}, status=401)
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Address
from .serializers import AddressSerializer
from rest_framework.permissions import IsAuthenticated

class AddressList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        addresses = Address.objects.all()
        serializer = AddressSerializer(addresses, many=True)
        return Response(serializer.data)

    def post(self, request):
        # Accessing data using request.data.get()
        name = request.data.get('newname')
        phone = request.data.get('phone')
        address = request.data.get('address')
        city = request.data.get('city')
        state = request.data.get('state')
        country = request.data.get('country')
        zip_code = request.data.get('zip_code')
        user_id = request.data.get('user_id')

        # Check if user_id is provided and if it is a valid user ID
        if not user_id:
            return Response({"error": "User ID is required."}, status=400)
        try:
            user = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            return Response({"error": "Invalid User ID."}, status=400)

        # Create the Address object
        address_obj = Address.objects.create(
            newname=name,
            phone=phone,
            address=address,
            city=city,
            state=state,
            country=country,
            zip_code=zip_code,
            status=1,
            user_id=user
        )

        return Response({"message": "Address created successfully."}, status=201)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_delivery_time(request):

    address_id = request.data.get('address_id')
    new_delivery_time = request.data.get('delivery_time')

    if not address_id:
        return Response({"error": "Address ID is required."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        address = Address.objects.get(pk=address_id)
    except Address.DoesNotExist:
        return Response({"error": "Address not found."}, status=status.HTTP_404_NOT_FOUND)

    if new_delivery_time:
        address.delivery_time = new_delivery_time
        address.save()
        return Response({"message": "Delivery time updated successfully."}, status=status.HTTP_200_OK)
    else:
        return Response({"error": "Delivery time not provided."}, status=status.HTTP_400_BAD_REQUEST)