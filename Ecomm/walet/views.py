from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from ecomApp.models import CustomUser
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from .models import PurchaseBenefit

# Create your views here.
class WalletAPIView(View):
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        user_id = request.GET.get('user_id')

        if not user_id:
            return JsonResponse({'error': 'User ID parameter is missing'}, status=400)

        try:
            wallet_instance = Walet.objects.get(user_id=user_id)

            wallet_value = wallet_instance.wallet_value
            return JsonResponse({'wallet_value': wallet_value})
        except Walet.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from ecomApp.models import CustomUser
from .models import Walet
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

class UpdateWallet(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user_id = request.data.get('user_id')

        # Check if user exists
        try:
            user = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            return Response({"error": "User does not exist."}, status=status.HTTP_400_BAD_REQUEST)

        wallet, created = Walet.objects.get_or_create(user_id=user.id)

        # Get amount to subtract from the wallet
        try:
            amount_to_subtract = user.walet
        except AttributeError:
            return Response({"error": "Wallet amount not provided."}, status=status.HTTP_400_BAD_REQUEST)


        wallet.wallet_value += amount_to_subtract
        wallet.save()
        user.walet-=amount_to_subtract
        user.save()
        return Response({"success"})
from decimal import Decimal
from decimal import Decimal

def calculate_purchase_benefit(user_id, total_amount):
    max_benefit_percentage = Decimal('0')
    wallet_value = Decimal('0')

    # Fetch purchase benefits and iterate through them
    purchase_benefits = PurchaseBenefit.objects.filter(status='1')

    for benefit in purchase_benefits:
        if total_amount >= Decimal(benefit.price) and benefit.benefit_percentage > max_benefit_percentage:
            max_benefit_percentage = Decimal(benefit.benefit_percentage)
            wallet_value =  Decimal(total_amount) * (max_benefit_percentage / Decimal('100'))

    # Convert wallet_value to int if necessary
    wallet_value = int(wallet_value)

    # Update wallet model amount
    try:
        wallet = Walet.objects.get(user_id=user_id)
        wallet.wallet_value += wallet_value
        wallet.save()
    except Walet.DoesNotExist:
        Walet.objects.create(user_id=user_id, wallet_value=wallet_value)

    return max_benefit_percentage, wallet_value
