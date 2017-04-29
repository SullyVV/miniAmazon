from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Whstock(models.Model):
    wid = models.BigIntegerField(default=1000)
    hid = models.IntegerField(default=-1)
    ctlg_id = models.IntegerField(default=-1)
    ctlg = models.CharField(max_length=100, default="")
    pid = models.BigIntegerField(default=-1)
    dsc = models.CharField(max_length=100, default="")
    count = models.BigIntegerField(default=-1)
    href = models.CharField(max_length=500, default="")
    def __str__(self):
        return "product_id: " + str(self.pid) + "   " + "product_description: " + self.dsc + "   " + "product_count: " + str(self.count)

class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_name = models.CharField(max_length=100)
    address_x = models.IntegerField(default=-1)
    address_y = models.IntegerField(default=-1)
    ups_act = models.IntegerField(default=-1)
    stock = models.ForeignKey(Whstock, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=100, default="")
    product_num = models.IntegerField(default=-1)
    ship_id = models.IntegerField(default=-1)
    package_id = models.IntegerField(default=-1)
    arrived = models.BooleanField(default=False)
    ready = models.BooleanField(default=False)
    loaded = models.BooleanField(default=False)
