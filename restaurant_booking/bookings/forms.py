from django import forms
from .models import Reservation
from datetime import time

class ReservationForm(forms.ModelForm):
    name = forms.CharField(label='Your Name', max_length=100)
    phone_number = forms.CharField(label='Phone Number', max_length=20)
    guests = forms.IntegerField(label='Number of Guests', min_value=1, widget=forms.NumberInput(attrs={'type': 'number', 'min': '1', 'max': '10', 'step': '1'}))
    date = forms.DateField(label='Date', widget=forms.SelectDateWidget())
    time = forms.ChoiceField(label='Time', choices=[(time(hour, 0).strftime('%H:%M'), time(hour, 0).strftime('%I:%M %p')) for hour in range(9, 23)])

    class Meta:
        model = Reservation
        fields = ['name', 'phone_number', 'guests', 'date', 'time']
