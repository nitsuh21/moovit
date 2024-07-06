from django.shortcuts import render

# Create your views here.
def overview(request):
    if request.method == 'POST':
        print(request.POST)
    else:
        return render(request, 'dashboard/overview.html')
    
def orders(request):
    if request.method == 'POST':
        print(request.POST)
    else:
        return render(request, 'dashboard/orders.html')

def drivers(request):
    if request.method == 'POST':
        print(request.POST)
    else:
        return render(request, 'dashboard/drivers.html')

def driver_profile(request, id):
    if request.method == 'POST':
        print(request.POST)
    else:
        return render(request, 'dashboard/driver_profile.html')