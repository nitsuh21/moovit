from django.urls import path

from . import views

urlpatterns = [
    path('overview/', views.overview, name='overview'),
    path('drivers/', views.drivers, name='drivers'),
    path('orders/', views.orders, name='orders'),
    path('driver-profile/<str:id>/', views.driver_profile, name='driver_profile'),
]