from django.shortcuts import render, redirect
from orders.models import Order
from home.models import Driver
from django.db.models import Sum
from django.utils import timezone
from datetime import timedelta

now = timezone.now()
start_of_month = now.replace(day=1)
end_of_month = (start_of_month + timedelta(days=32)).replace(day=1) - timedelta(days=1)

def overview(request):
    if request.method == 'POST':
        print(request.POST)
    else:
        if request.user.is_authenticated:
            total_orders = Order.objects.all().count()
            total_complete_orders = Order.objects.filter(order_status='delivered').count()
            total_intiated_orders = Order.objects.filter(order_status='Intiated').count()
            total_pending_orders = Order.objects.filter(order_status='pending').count()
            total_incomplete_orders = total_intiated_orders + total_pending_orders
            total_transactions_count = Order.objects.filter(payment_status='paid').count()
            total_transactions_value = Order.objects.filter(payment_status='paid').aggregate(Sum('price'))
            total_pending_transactions = Order.objects.filter(payment_status='pending').count()
            total_customers = Order.objects.values('sender_email').distinct().count()
            new_customers_count = Order.objects.filter(
                created_at__gte=start_of_month,
                created_at__lte=end_of_month
            ).values('sender_email').distinct().count()
            total_drivers = Driver.objects.all().count()
            active_drivers = Driver.objects.filter(available=True).count()

            context = {
                'total_orders': total_orders,
                'total_complete_orders': total_complete_orders,
                'total_intiated_orders': total_intiated_orders,
                'total_pending_orders': total_pending_orders,
                'total_incomplete_orders': total_incomplete_orders,
                'total_transactions_count': total_transactions_count,
                'total_transactions_value': total_transactions_value,
                'total_pending_transactions': total_pending_transactions,
                'total_customers': total_customers,
                'new_customers_count': new_customers_count,
                'total_drivers': total_drivers,
                'active_drivers': active_drivers
            }

            return render(request, 'dashboard/overview.html', context)
        else:
            return redirect('signin')
    
def orders(request):
    if request.method == 'POST':
        print(request.POST)
    else:
        orders = Order.objects.all().order_by('-id')
        context = {
            'orders': orders
        }
        return render(request, 'dashboard/orders.html',context)

def order_details(request, orderID):
    if request.method == 'POST':
        orderID = request.POST.get('orderID')
        item_name = request.POST.get('item_name')
        item_type = request.POST.get('item_type')
        height = request.POST.get('height')
        width = request.POST.get('width')
        length = request.POST.get('length')
        weight = request.POST.get('weight')
        quantity = request.POST.get('quantity')
        order_date = request.POST.get('order_date')
        pickup_address = request.POST.get('pickup_address')
        delivery_address = request.POST.get('delivery_address')
        pickup_date = request.POST.get('pickup_date')
        delivery_date = request.POST.get('delivery_date')
        pickup_time = request.POST.get('pickup_time')
        payment_status = request.POST.get('payment_status')
        order_status = request.POST.get('order_status')
        complain_status = request.POST.get('complain_status')
        price = request.POST.get('price')
        sender_name = request.POST.get('sender_name')
        sender_email = request.POST.get('sender_email')
        sender_phone = request.POST.get('sender_phone')
        receiver_name = request.POST.get('receiver_name')
        receiver_email = request.POST.get('receiver_email')
        receiver_phone = request.POST.get('receiver_phone')
        description = request.POST.get('description')
        driver_assigned = request.POST.get('driver_assigned')

        print(orderID, item_name, item_type, height, width, length, weight, quantity, order_date, pickup_address, delivery_address, pickup_date, delivery_date, pickup_time, payment_status, order_status, complain_status, price, sender_name, sender_email, sender_phone, receiver_name, receiver_email, receiver_phone, description, driver_assigned)
        try:
            order = Order.objects.get(orderID=orderID)
        except Exception as e:
            return redirect('orders')

        order.item_name = item_name
        order.item_type = item_type
        order.height = height
        order.width = width
        order.length = length
        order.weight = weight
        order.quantity = quantity
        order.order_date = order_date
        order.pickup_address = pickup_address
        order.delivery_address = delivery_address
        order.pickup_date = pickup_date
        order.delivery_date = delivery_date
        order.pickup_time = pickup_time
        order.payment_status = payment_status
        order.order_status = order_status
        order.complain_status = complain_status
        order.price = price
        order.sender_name = sender_name
        order.sender_email = sender_email
        order.sender_phone = sender_phone
        order.receiver_name = receiver_name
        order.receiver_email = receiver_email
        order.receiver_phone = receiver_phone
        order.description = description
        order.driver_assigned = driver_assigned
        order.save()

        return redirect('order_details', orderID)
    else:
        order = Order.objects.get(orderID=orderID)
        context = {
            'order': order
        }
        return render(request, 'dashboard/order_details.html', context)
def drivers(request):
    if request.method == 'POST':
        print(request.POST)
    else:
        return render(request, 'dashboard/drivers.html')

def profile_details(request, id):
    if request.method == 'POST':
        print(request.POST)
    else:
        return render(request, 'dashboard/profile_details.html')