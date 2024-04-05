from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from ecomApp.models import CustomUser
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

# Create your views here.
class WalletAPIView(View):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_id = request.GET.get('user_id')
        if not user_id:
            return JsonResponse({'error': 'User ID parameter is missing'}, status=400)

        try:
            user = CustomUser.objects.get(pk=user_id)
            wallet_value = user.walet
            return JsonResponse({'wallet_value': wallet_value})
        except CustomUser.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from ecomApp.models import CustomUser
from .models import Walet
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
@permission_classes([IsAuthenticated])
def save_and_update_wallet(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_id = data.get('user_id')
            amount=0
            if not user_id:
                return JsonResponse({'error': 'User ID or amount is missing'}, status=400)

            user = CustomUser.objects.get(pk=user_id)
            amount = user.walet # Retrieve wallet_value from CustomUser object

            # Update the user's wallet value
            user.walet -= amount
            user.save()

            # Save the wallet transaction
            Walet.objects.create(user_id=user.id, wallet_value=amount)

            return JsonResponse({'success': 'Wallet transaction saved and wallet updated successfully'})
        except (CustomUser.DoesNotExist, json.JSONDecodeError, ValueError):
            return JsonResponse({'error': 'Invalid request data or user not found'}, status=400)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)
