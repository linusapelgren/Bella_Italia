# bookings/urls.py

from django.urls import path
from .views import index, make_reservation, reservation_confirmation, menu, get_available_times

urlpatterns = [
    path('', index, name='index'),
    path('make-reservation/', make_reservation, name='make_reservation'),
    path('reservation-confirmation/<int:reservation_id>/', reservation_confirmation, name='reservation_confirmation'),
    path('menu/', menu, name='menu'),
    path('get-available-times/', get_available_times, name='get_available_times'),
]
