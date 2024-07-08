from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


# Create your views here.
def home(request):
    return render(request, 'home.html')

def contactus(request):
    return render(request, 'contact-us.html')

def aboutus(request):
    return render(request, 'about-us.html')

def pricing(request):
    return render(request, 'pricing.html')

def signin(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not email:
            return render(request, 'signin.html', {'error': 'Email is required'})
        if not password:
            return render(request, 'signin.html', {'error': 'Password is required'})

        # Authenticate the user
        user = authenticate(email=email, password=password)
        if user is not None:
            #check if the user is a driver
            if user.user_role == 'driver':
                return redirect('driver_dashboard')
            login(request, user)
            return redirect('overview') 
        else:
            messages.error(request, 'Invalid Email or Password')
            return render(request, 'signin.html')
    else:
        return render(request, 'signin.html')
    
def signout(request):
    logout(request)
    return redirect('signin')

