from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('contactus', views.contactus, name='contactus' ),
    path('signin', views.signin, name='signin'),
    path('signout', views.signout, name='signout'),
]