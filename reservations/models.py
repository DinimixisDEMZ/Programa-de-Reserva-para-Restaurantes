from django.db import models
from tables.models import Table

# Create your models here.

class Reservation(models.Model):
    customer_name = models.CharField(max_length=100)
    customer_phone = models.CharField(max_length=20)
    customer_email = models.EmailField(blank=True)
    date = models.DateField()
    time = models.TimeField()
    guests = models.IntegerField()
    table = models.ForeignKey(Table, on_delete=models.SET_NULL, null=True)
    notes = models.TextField(blank=True)
    status = models.CharField(max_length=20, default='confirmed')
