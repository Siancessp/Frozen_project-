# serializers.py
from rest_framework import serializers
from ecomApp.models import CustomUser
# class RegistrationSerializer(serializers.Serializer):
#     phone_number = serializers.CharField()
#     otp = serializers.CharField()
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['phone_number', 'password']