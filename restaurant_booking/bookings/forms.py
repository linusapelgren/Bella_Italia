# bookings/forms.py

from django import forms
from .models import Reservation
from datetime import datetime

class ReservationForm(forms.ModelForm):
    name = forms.CharField(label='Your Name', max_length=100)
    phone_number = forms.CharField(label='Phone Number', max_length=20)
    guests = forms.IntegerField(label='Number of Guests', min_value=1, widget=forms.NumberInput(attrs={'type': 'number', 'min': '1', 'max': '10', 'step': '1'}))
    date = forms.DateField(label='Date', widget=forms.DateInput(attrs={'class': 'datepicker'}))
    time = forms.ChoiceField(label='Time', choices=[])

    def __init__(self, *args, **kwargs):
        fetch_available_times = kwargs.pop('fetch_available_times', None)  # Fetch function from kwargs
        super().__init__(*args, **kwargs)
        
        if 'initial' in kwargs and 'date' in kwargs['initial']:
            date = kwargs['initial']['date']
        else:
            date = datetime.today().date()

        # Fetch available times based on the provided date using the function passed
        if fetch_available_times:
            available_times = fetch_available_times(date)
        else:
            available_times = []

        # Populate choices for the time field
        self.fields['time'].choices = [(time_slot, time_slot) for time_slot in available_times]

        # Set initial value for the date field
        self.fields['date'].initial = date

    class Meta:
        model = Reservation
        fields = ['name', 'phone_number', 'guests', 'date', 'time']
