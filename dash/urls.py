from django.urls import path

from . import views

urlpatterns = [
    path('overview/', views.overview, name='overview'),
    path('drivers/', views.drivers, name='drivers'),
    path('orders/', views.orders, name='orders'),
    path('order_details/<str:orderID>/', views.order_details, name="order_details"),
    path('profiles/<str:id>/', views.profile_details, name='profile_details'),
]