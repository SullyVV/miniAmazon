from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Whstock(models.Model):
    whnum = models.BigIntegerField(default=-1)
    hid = models.IntegerField(default=-1)
    pid = models.BigIntegerField(default=-1)
    dsc = models.CharField(max_length=100)
    count = models.BigIntegerField(default=-1)
    def __str__(self):
        return "product_id: " + str(self.pid) + "   " + "product_description: " + self.dsc + "   " + "product_num: " + str(self.num)

class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_name = models.CharField(max_length=100)
    stock = models.ForeignKey(Whstock, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=100, default="")
    product_num = models.IntegerField(default=-1)
    ship_id = models.IntegerField(default=-1)
    package_id = models.IntegerField(default=-1)
    arrived = models.BooleanField(default=False)
    ready = models.BooleanField(default=False)
    loaded = models.BooleanField(default=False)
