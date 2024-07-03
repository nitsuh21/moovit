from django.db import models
from home.models import User, Driver, Customer

# Create your models here.
class Order(models.Model):
    item_name = models.CharField(max_length=100, null=True, blank=True)
    item_type = models.CharField(max_length=100, default="Parcel")
    orderID = models.CharField(max_length=100)
    height = models.IntegerField(default=0)
    width = models.IntegerField(default=0)
    length = models.IntegerField(default=0)
    weight = models.IntegerField(default=0)
    quantity = models.IntegerField(default=1)
    order_date = models.DateField(auto_now_add = True)

    pickup_address = models.CharField(max_length=100)
    delivery_address = models.CharField(max_length=100)
    pickup_date = models.DateField(null=True, blank=True)
    delivery_date = models.DateField(null=True, blank=True)
    pickup_time = models.TimeField(null=True, blank=True)
    payment_status = models.CharField(max_length=100, default="Pending")
    order_status = models.CharField(max_length=100, default="Initiated")
    complain_status = models.CharField(max_length=100, default="No")

    #contact information
    sender_name = models.CharField(max_length=100, blank=True, null=True)
    sender_email = models.EmailField(blank=True, null=True)
    sender_phone = models.CharField(max_length=100, blank=True, null=True)
    receiver_name = models.CharField(max_length=100, blank=True, null=True)
    receiver_email = models.EmailField(blank=True, null=True)
    receiver_phone = models.CharField(max_length=100, blank=True, null=True)

    description = models.TextField(default="No description provided")

    driver_assigned = models.ForeignKey(Driver, on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return self.item_name