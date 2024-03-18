
from django.db import models
from django.contrib.auth.models import User
from ecomApp.models import CustomUser
from ecomApp.models import Catagory
from ecomApp.models import Product
from django.conf import settings
from menu_management.models import Item

class Order(models.Model):

    id = models.AutoField(primary_key=True)
    order_id=models.CharField(max_length=50)
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,null=True)#made CustomUser later
    cat_id = models.ForeignKey(Catagory, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Item, on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=100)
    couponcode = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.IntegerField()
    quantity=models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return  f"{self.id}"
