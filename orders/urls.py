from django.urls import path

from . import views

urlpatterns = [
    path('/createOrder', views.create_order, name='create_order'),
]