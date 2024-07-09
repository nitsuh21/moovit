from django.shortcuts import render, redirect
from .models import Order
import random
import string
import datetime
from django.contrib import messages
from django.core.mail import send_mail
from geopy.geocoders import GoogleV3
from geopy.distance import geodesic
from datetime import datetime, timedelta

google_api_key = 'AIzaSyBi4BjJLG_eFOenyKILydQDQ2YxrSTgXHo'

def get_coordinates_google(address, api_key):
    geolocator = GoogleV3(api_key=api_key)
    try:
        location = geolocator.geocode(address)
        if location:
            return (location.latitude, location.longitude)
        else:
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None


def calculate_distance(pickup, delivery):
    return geodesic(pickup, delivery).kilometers

def estimate_delivery_time(distance):
    average_speed_kmh = 60
    hours = distance / average_speed_kmh
    return timedelta(hours=hours)

def calculate_price(distance):
    base_price = 5.0  # Base price in euros
    price_per_km = 0.50  # Price per kilometer in euros
    return base_price + (distance * price_per_km)



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

        # pickup_address = request.get.POST("pickup_address")
        # delivery_address = request.get.POST("delivery_address")
        # pickup_date = request.get.POST("pickup_date")
        estimated_delivery_datetime = request.POST.get('estimated_delivery_datetime')
        if estimated_delivery_datetime:
            estimated_delivery_datetime = estimated_delivery_datetime.replace('a.m.', 'AM').replace('p.m.', 'PM')
            estimated_delivery_datetime = datetime.strptime(estimated_delivery_datetime, '%B %d, %Y, %I:%M %p').date()
        else:
            estimated_delivery_datetime = None
        price = float(request.POST["price"])

        print("sender_name", sender_name, "sender_email", sender_email, "sender_phone", sender_phone, "receiver_name", receiver_name, "receiver_email", receiver_email, "receiver_phone", receiver_phone, "estimated_delivery_datetime", estimated_delivery_datetime, "price", price)

        payment_status = "Paid"

        order = Order.objects.get(orderID=orderid)
        order.sender_name = sender_name
        order.sender_email = sender_email
        order.sender_phone = sender_phone
        order.receiver_name = receiver_name
        order.receiver_email = receiver_email
        order.receiver_phone = receiver_phone
        order.payment_status = payment_status
        order.delivery_date = estimated_delivery_datetime
        order.price = price

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
            pickup_loc = order.pickup_address
            delivery_loc = order.delivery_address

            pickup_coordinates = get_coordinates_google(pickup_loc, google_api_key)
            delivery_coordinates = get_coordinates_google(delivery_loc, google_api_key)

            print('locations',pickup_coordinates, delivery_coordinates)

            distance = calculate_distance(pickup_coordinates, delivery_coordinates)

            estimated_time = estimate_delivery_time(distance)
            estimated_delivery_datetime = datetime.now() + estimated_time

            price = calculate_price(distance)

            price = round(price, 2)


        except Order.DoesNotExist:
            return redirect('home')
        
        context = {
            "order": order,
            "estimated_delivery_datetime": estimated_delivery_datetime,
            "price": price
        }
        return render(request, 'checkout.html', context)
    
def track_order(request):
    if request.method == 'POST':
        orderID = request.POST['order_id']
        try:
            order = Order.objects.get(orderID=orderID)
            if order is not None:
                context = {
                'order': order
                }
                return render(request, 'tracking-result.html', context)
            else:
                messages.error(request, 'Order not found')
                return redirect('track_order')
        except Order.DoesNotExist:
            messages.error(request, 'Order not found')
            return redirect('track_order')
    else:
        return render(request, 'tracking-result.html')