from django.shortcuts import render, redirect
from .models import Order
import random
import string
import datetime
from django.contrib import messages
from django.core.mail import send_mail
from geopy.geocoders import Nominatim

loc = Nominatim(user_agent="GetLoc")

def get_pickup_address():
    return "Pickup Address"

def get_delivery_address():
    return "Delivery Address"

def get_pickup_date():
    return '2020-05-12'

def get_delivery_date():
    return '2020-05-12'

# Create your views here.
def create_order(request):
    if request.method == 'POST':
        pickup_address = request.POST['pickup_address']
        delivery_address = request.POST['delivery_address']
        weight = request.POST['weight']
        height = request.POST['height']
        width = request.POST['width']
        length = request.POST['length']

        orderID = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        
        print(pickup_address, delivery_address, weight, height, width, length, orderID)
        try:
            order = Order.objects.create(pickup_address=pickup_address, delivery_address=delivery_address, weight=weight, height=height, width=width, length=length, orderID=orderID)
            order.save()
            return redirect('checkout', orderID)
        except Exception as e:
            messages.error(request, 'Error creating order')
            return redirect('home')
    else:
        return render(request, 'create.html')


def checkout_order(request, orderid):
    if request.method == 'POST':
        sender_name = request.POST['sender_name']
        sender_email = request.POST['sender_email']
        sender_phone = request.POST['sender_phone']

        receiver_name = request.POST['receiver_name']
        receiver_email = request.POST['receiver_email']
        receiver_phone = request.POST['receiver_phone']

        pickup_address = get_pickup_address()
        delivery_address = get_delivery_date()
        pickup_date = get_pickup_date()
        delivery_date = get_delivery_date()

        payment_status = "Paid"

        order = Order.objects.get(orderID=orderid)
        order.sender_name = sender_name
        order.sender_email = sender_email
        order.sender_phone = sender_phone
        order.receiver_name = receiver_name
        order.receiver_email = receiver_email
        order.receiver_phone = receiver_phone
        order.pickup_address = pickup_address
        order.delivery_address = delivery_address 
        order.pickup_date = pickup_date
        order.delivery_date = delivery_date 
        order.payment_status = payment_status

        order.save()

        # try:
        #     send_mail(
        #         'Order Confirmation',  # subject
        #         'Your order has been placed successfully.',  # message
        #         'blenderthesky12@gmail.com',  # from email
        #         [order.sender_email],  # to email
        #     )
        # except:
        #     pass

        messages.success(request, 'Your order Placed Successfully, we have sent you an email with the order details')
        return redirect('home')
    else:
        try:
            order = Order.objects.get(orderID=orderid)
            pickup_loc = loc.geocode(order.pickup_address)
            delivery_loc = loc.geocode(order.delivery_address)

            print(pickup_loc, delivery_loc)
        except Order.DoesNotExist:
            return redirect('home')
        
        context = {
            "order": order
        }
        return render(request, 'checkout.html', context)
    
