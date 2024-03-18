# serializers.py
from rest_framework import serializers
from ecomApp.models import CustomUser
# class RegistrationSerializer(serializers.Serializer):
#     phone_number = serializers.CharField()
#     otp = serializers.CharField()
class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=8, write_only=True)

    class Meta:
        model = CustomUser
        fields = ('phone_number',  'password')

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user
