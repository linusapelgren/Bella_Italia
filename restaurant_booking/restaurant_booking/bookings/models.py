# bookings/models.py
from django.db import models

class Reservation(models.Model):
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    guests = models.IntegerField()
    date = models.DateField()
    time = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.name} - {self.date} - {self.time}"
