from django import forms
from .models import Reservation
from django.forms import DateInput, TimeInput
from datetime import date, time
from django.core.exceptions import ValidationError

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
        widgets = {
            'date': DateInput(
                attrs={
                    'type': 'date',
                    'class': 'form-control datepicker',
                    'min': date.today().strftime('%Y-%m-%d')  # No permite fechas pasadas
                },
                format='%Y-%m-%d'
            ),
            'time': TimeInput(
                attrs={
                    'type': 'time',
                    'class': 'form-control timepicker',
                    'min': '08:00',  # Hora de apertura
                    'max': '23:00'    # Hora de cierre
                },
                format='%H:%M'
            ),
            'notes': forms.Textarea(attrs={
                'rows': 3,
                'class': 'form-control',
                'placeholder': 'Indique cualquier requerimiento especial...'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Añadir clases Bootstrap a todos los campos
        for field_name, field in self.fields.items():
            if 'class' not in field.widget.attrs:
                field.widget.attrs['class'] = 'form-control'
        
        # Placeholders específicos
        self.fields['customer_name'].widget.attrs['placeholder'] = 'Nombre completo'
        self.fields['customer_phone'].widget.attrs['placeholder'] = 'Ej: +52 55 1234 5678'
        self.fields['customer_email'].widget.attrs['placeholder'] = 'ejemplo@correo.com'
        self.fields['guests'].widget.attrs['min'] = 1
        self.fields['guests'].widget.attrs['max'] = 20  # Asumiendo un máximo de 20 personas
        
        # Ordenar las mesas de forma más amigable
        self.fields['table'].queryset = self.fields['table'].queryset.order_by('number_of_chairs')
    
    def clean_date(self):
        date_val = self.cleaned_data.get('date')
        if date_val and date_val < date.today():
            raise ValidationError("No se pueden hacer reservaciones para fechas pasadas.")
        return date_val
    
    def clean_time(self):
        time_val = self.cleaned_data.get('time')
        if time_val:
            opening_time = time(8, 0)  # 8:00 AM
            closing_time = time(23, 0)  # 11:00 PM
            if not (opening_time <= time_val <= closing_time):
                raise ValidationError("El horario debe estar entre 8:00 AM y 11:00 PM")
        return time_val
    
    def clean(self):
        cleaned_data = super().clean()
        date_val = cleaned_data.get('date')
        time_val = cleaned_data.get('time')
        table_val = cleaned_data.get('table')
        
        # Validar disponibilidad de mesa
        if all([date_val, time_val, table_val]):
            conflicting = Reservation.objects.filter(
                date=date_val,
                time=time_val,
                table=table_val,
                status=Reservation.ReservationStatus.CONFIRMED
            )
            
            # Excluir la instancia actual si estamos editando
            if self.instance.pk:
                conflicting = conflicting.exclude(pk=self.instance.pk)
            
            if conflicting.exists():
                raise ValidationError({
                    'table': 'Esta mesa ya está reservada para la fecha y hora seleccionada'
                })
        
        return cleaned_data