from django.db import models

# Create your models here.
class Order(models.Model):
    item_name = models.CharField(max_length=100)
    item_type = models.CharField(max_length=100)
    height = models.IntegerField()
    width = models.IntegerField()
    length = models.IntegerField()
    weight = models.IntegerField()
    quantity = models.IntegerField()
    order_date = models.DateField(auto_now_add = True)

    pickup_address = models.CharField(max_length=100)
    delivery_address = models.CharField(max_length=100)
    pickup_date = models.DateField()
    delivery_date = models.DateField()
    pickup_time = models.TimeField()
    delivery_status = models.CharField(max_length=100)

    #contact information
    sender_name = models.CharField(max_length=100)
    sender_email = models.EmailField()
    sender_phone = models.CharField(max_length=100)
    receiver_name = models.CharField(max_length=100)
    receiver_email = models.EmailField()
    receiver_phone = models.CharField(max_length=100)

    description = models.TextField()
    
    def __str__(self):
        return self.item_name