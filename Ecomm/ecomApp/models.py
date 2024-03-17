from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.shortcuts import reverse
from django.utils import timezone
from decimal import Decimal
import random
from django.contrib.auth.models import User
class CustomUserManager(BaseUserManager):
    def create_user(self, phone_number, password=None, **extra_fields):
        if not phone_number:
            raise ValueError('The phone_number must be set')

        phone_number = self.normalize_phone_number(phone_number)
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number,  password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(phone_number, phone_number, password, **extra_fields)

class CustomUser(AbstractBaseUser):
    id = models.AutoField(primary_key=True)
    otp = models.CharField(max_length=6, blank=True)
    phone_number = models.CharField(max_length=16,unique=True)
    password = models.CharField(max_length=128)  # No need to store password directly
    status = models.BooleanField(default=False)
    name = models.CharField(max_length=50, blank=True)
    address = models.TextField(blank=True)
    # gender=models.BooleanField(blank=True)
    profile_photo=models.ImageField(upload_to='images/', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['phone_number']

    def __str__(self):
        return self.phone_number

    class Meta:
        ordering = ['phone_number']  # Adjust ordering field

class Otp(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    email_verified = models.BooleanField(default=False)
    otp = models.CharField(max_length=6, blank=True)
    otp_created_at = models.DateTimeField(null=True, blank=True)
class Stock(models.Model):
    id = models.BigAutoField(primary_key=True)
    openingstock=models.TextField()
    item_id=models.TextField()
  #  pro_id= models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class Catagory(models.Model):
    id = models.AutoField(primary_key=True)
    name= models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/')
    status= models.BooleanField(default=True)
    # uploaded_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name


class Product(models.Model):
    id = models.BigAutoField(primary_key=True)

    name= models.CharField(max_length=100)
    cat_name = models.ForeignKey(Catagory,on_delete=models.CASCADE)
    price=models.IntegerField()
    coupon = models.IntegerField( blank=True, null=True)
    description=models.CharField(max_length=500)
    image = models.ImageField(upload_to='images/')
    status= models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    barcode = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.name


class CustomerCoupon(models.Model):
    id = models.AutoField(primary_key=True)
    customer =  models.CharField(max_length=255)
    occasion = models.CharField(max_length=255)
    expire_date = models.DateField()
    coupon_value = models.CharField(max_length=255)
    coupon_type = models.CharField(max_length=20)
    description = models.TextField()
    status= models.BooleanField(default=True)
