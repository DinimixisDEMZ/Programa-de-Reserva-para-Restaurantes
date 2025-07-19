from django.db import models
from tables.models import Table

# Create your models here.

class ReservationStatus(models.IntegerChoices):
    CANCELED = 0, 'Cancelado'
    CONFIRMED = 1, 'Confirmado'

class Reservation(models.Model):
    customer_name = models.CharField(max_length=100)
    customer_phone = models.CharField(max_length=20)
    customer_email = models.EmailField(blank=True)
    date = models.DateField()
    time = models.TimeField()
    guests = models.IntegerField()
    table = models.ForeignKey(Table, on_delete=models.SET_NULL, null=True)
    notes = models.TextField(blank=True)
    status = models.IntegerField(choices=ReservationStatus.choices, default=ReservationStatus.CONFIRMED)

    def __str__(self):
        return  f"{self.customer_name} {self.get_status_display()}"
