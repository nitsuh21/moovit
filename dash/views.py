from django.shortcuts import render, redirect
from orders.models import Order
from home.models import Driver, User
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
            total_complete_orders = Order.objects.filter(order_status='Delivered').count()
            total_intiated_orders = Order.objects.filter(order_status='Initiated').count()
            total_pending_orders = Order.objects.filter(order_status='Pending').count()
            total_cancelled_orders = Order.objects.filter(order_status='Cancelled').count()
            total_incomplete_orders = total_intiated_orders + total_pending_orders
            total_transactions_count = Order.objects.filter(payment_status='Paid').count()
            total_transactions_value = Order.objects.filter(payment_status='Paid').aggregate(Sum('price'))['price__sum']
            total_pending_transactions = Order.objects.filter(payment_status='pending').count()
            total_customers = Order.objects.values('sender_email').distinct().count()
            new_customers_count = Order.objects.filter(
                created_at__gte=start_of_month,
                created_at__lte=end_of_month
            ).values('sender_email').distinct().count()
            total_drivers = Driver.objects.all().count()
            active_drivers = Driver.objects.filter(available=True).count()

            #recent orders
            recent_orders = Order.objects.all().order_by('-id')[:10]

            #top drivers
            top_drivers = Driver.objects.all().order_by('-points')[:5]

            context = {
                'total_orders': total_orders,
                'total_complete_orders': total_complete_orders,
                'total_intiated_orders': total_intiated_orders,
                'total_pending_orders': total_pending_orders,
                'total_cancelled_orders': total_cancelled_orders,
                'total_incomplete_orders': total_incomplete_orders,
                'total_transactions_count': total_transactions_count,
                'total_transactions_value': total_transactions_value,
                'total_pending_transactions': total_pending_transactions,
                'total_customers': total_customers,
                'new_customers_count': new_customers_count,
                'total_drivers': total_drivers,
                'active_drivers': active_drivers,
                'recent_orders': recent_orders,
                'top_drivers': top_drivers
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
        #order_date = request.POST.get('order_date')
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
        print("dr_ssigned", driver_assigned)
        driver_user = User.objects.filter(email=driver_assigned)
        driver_assigned = Driver.objects.get(user__in=driver_user)

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
        #order.order_date = order_date
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

        return redirect('orders')
    else:
        order = Order.objects.get(orderID=orderID)
        drivers = Driver.objects.filter(available=True)
        print("drivers", drivers)
        context = {
            'order': order,
            'drivers': drivers
        }
        return render(request, 'dashboard/order_details.html', context)

def drivers(request):
    if request.method == 'POST':
        print(request.POST)
    else:
        drivers = Driver.objects.all().order_by('-user_id')
        context = {
            'drivers': drivers
        }
        return render(request, 'dashboard/drivers.html', context)

def profile_details(request, id):
    if request.method == 'POST':
        print(request.POST)
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        user = User.objects.get(email=id)
        user.email = email
        user.phone = phone
        user.address = address
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        return redirect('profile_details', email=email)

    else:
        first_name, last_name = id.split('-')
        try:
            user = User.objects.get(first_name__iexact=first_name, last_name__iexact=last_name)
        except:
            pass
        print({user})
        try:
            check_driver = Driver.objects.filter(user=user)
            if check_driver:
                driver = Driver.objects.get(user=user)
            else:
                driver = None
        except:
            pass

        context = {
            'user': user,
            'driver': driver
        }
        return render(request, 'dashboard/profile_details.html', context)
    
def myprofile(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        user = User.objects.get(email=request.user.email)
        user.email = email
        user.phone = phone
        user.address = address
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        return redirect('myprofile')
    else:
        return render(request, 'dashboard/myprofile.html')