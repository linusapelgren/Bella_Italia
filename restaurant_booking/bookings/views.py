from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Restaurant, Reservation, Menu, Table
from .forms import ReservationForm
from django.contrib import messages


def index(request):
    return render(request, 'bookings/index.html')


def restaurant_detail(request):
    restaurant = Restaurant.objects.first() 
    return render(request, 'bookings/restaurant_detail.html', {'restaurant': restaurant})


def make_reservation(request):
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            available_tables = Table.objects.filter(restaurant=Restaurant.objects.first(), capacity__gte=reservation.guests)
            conflicting_reservations = Reservation.objects.filter(date=reservation.date, time=reservation.time, table__in=available_tables)
            if conflicting_reservations.exists():
                messages.error(request, "No available tables at the selected time.")
            else:
                for table in available_tables:
                    if not Reservation.objects.filter(date=reservation.date, time=reservation.time, table=table).exists():
                        reservation.table = table
                        break
                if reservation.table:
                    reservation.user = request.user
                    reservation.save()
                    return redirect('reservation_confirmation', pk=reservation.pk)
                else:
                    messages.error(request, "No available tables at the selected time.")
    else:
        form = ReservationForm()
    return render(request, 'bookings/make_reservation.html', {'form': form})


def reservation_confirmation(request, pk):
    reservation = get_object_or_404(Reservation, pk=pk)
    return render(request, 'bookings/reservation_confirmation.html', {'reservation': reservation})


def menu(request):
    restaurant = Restaurant.objects.first()  
    menu_items = Menu.objects.filter(restaurant=restaurant)
    return render(request, 'bookings/menu.html', {'restaurant': restaurant, 'menu_items': menu_items})
