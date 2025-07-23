from django import forms
from reservations.models import Reservation

class ReservationForm(forms.ModelForm):

    class Meta:
        model = Reservation
        fields = [
            'customer_name',
            'customer_phone',
            'customer_email',
            'date',
            'time',
            'guests',
            'table',
            'notes'
        ]