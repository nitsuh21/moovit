from django.urls import path

from . import views

urlpatterns = [
    path('createOrder', views.create_order, name='create_order'),
    path('checkout/<str:orderid>', views.checkout_order, name='checkout'),
    path('trackOrder', views.track_order, name='track_order'),
]