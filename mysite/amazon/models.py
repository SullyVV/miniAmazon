from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Whstock(models.Model):
    wid = models.BigIntegerField
    hid = models.IntegerField
    pid = models.BigIntegerField
    dsc = models.CharField(max_length=100)
    num = models.BigIntegerField
    def __str__(self):
        return "product_id: " + self.pid + "   " + "product_description: " + self.dsc + "   " + "product_num: " + self.num

class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_name = models.CharField(max_length=100)
    stock = models.ForeignKey(Whstock, on_delete=models.CASCADE)
    arrived = models.BooleanField
    ready = models.BooleanField
    loaded = models.BooleanField
