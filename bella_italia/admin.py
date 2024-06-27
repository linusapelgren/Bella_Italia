# bookings/admin.py

from django.contrib import admin
from .models import Reservation

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone_number', 'guests', 'date', 'time')
    list_display_links = ('name', 'phone_number')
    list_editable = ('guests',)
    search_fields = ('name', 'phone_number', 'date', 'time')
    list_filter = ('date', 'time', 'guests')
    ordering = ('-date', '-time')
    list_per_page = 20
