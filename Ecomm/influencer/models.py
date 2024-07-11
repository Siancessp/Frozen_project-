from django.db import models
class Influencer(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    passbook = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, unique=True)
    password = models.CharField(max_length=128)  # Make sure to handle password hashing
    address = models.TextField()
    type = models.CharField(max_length=10)
    commission = models.DecimalField(max_digits=10, decimal_places=2)
    code = models.CharField(max_length=50, unique=True)
    status= models.BooleanField(default=True)

    def __str__(self):
        return self.name
# Create your models here.
