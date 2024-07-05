from django.db import models

# Create your models here.
class Walet(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField(unique=True)
    wallet_value = models.FloatField(default=0.0)

class PurchaseBenefit(models.Model):
    id = models.AutoField(primary_key=True)
    status = models.CharField(max_length=50,default='1')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    benefit_percentage = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"PurchaseBenefit #{self.id}"