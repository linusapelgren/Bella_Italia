# bookings/views.py

from django.shortcuts import render, redirect, get_object_or_404
from .models import Reservation
from .forms import ReservationForm
from datetime import datetime
from django.http import JsonResponse
from .forms import fetch_available_times

from .forms import ReservationForm

def index(request):
    return render(request, 'bookings/index.html')

def make_reservation(request):
    fetch_available_times = some_function_to_fetch_times()
    form = ReservationForm(fetch_available_times=fetch_available_times)

def make_reservation(request):
    if request.method == 'POST':
        form = ReservationForm(request.POST, fetch_available_times=fetch_available_times)
        if form.is_valid():
            reservation = form.save()
            print(f"Reservation created: {reservation.id}")
            return redirect('reservation_confirmation', reservation_id=reservation.id)
        else:
            print("Form errors:", form.errors)  # Print form errors to debug
    else:
        form = ReservationForm(fetch_available_times=fetch_available_times)

    available_times = fetch_available_times(datetime.today().date())  # Fetch available times for today
    print("Available Times:", available_times)
    print("Form Choices:", form.fields['time'].choices)

    return render(request, 'bookings/make_reservation.html', {'form': form})

def reservation_confirmation(request, reservation_id):
    print(f"Confirming reservation: {reservation_id}")  # Check this in your server console
    reservation = get_object_or_404(Reservation, pk=reservation_id)
    return render(request, 'bookings/reservation_confirmation.html', {'reservation': reservation})

def menu(request):
    return render(request, 'bookings/menu.html')

def get_available_times(request):
    date_str = request.GET.get('date')
    date = datetime.strptime(date_str, '%Y-%m-%d').date()
    times = fetch_available_times(date)
    return JsonResponse({'times': times})
