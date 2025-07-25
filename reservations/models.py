from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import time
from tables.models import Table

class ReservationStatus(models.IntegerChoices):
    CANCELED = 0, 'Cancelado'
    CONFIRMED = 1, 'Confirmado'
    PENDING = 2, 'Pendiente'  # Nuevo estado útil para reservas no confirmadas

class Reservation(models.Model):
    customer_name = models.CharField(
        max_length=100,
        verbose_name='Nombre del cliente'
    )
    customer_phone = models.CharField(
        max_length=20,
        verbose_name='Teléfono'
    )
    customer_email = models.EmailField(
        blank=True,
        verbose_name='Correo electrónico'
    )
    date = models.DateField(
        verbose_name='Fecha de reservación'
    )
    time = models.TimeField(
        verbose_name='Hora de reservación'
    )
    guests = models.PositiveIntegerField(
        verbose_name='Número de personas',
        default=1
    )
    table = models.ForeignKey(
        Table,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Mesa',
        related_name='reservations'
    )
    notes = models.TextField(
        blank=True,
        verbose_name='Notas adicionales'
    )
    status = models.IntegerField(
        choices=ReservationStatus.choices,
        default=ReservationStatus.PENDING,  # Cambiado a PENDING por defecto
        verbose_name='Estado'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de creación'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Última actualización'
    )

    class Meta:
        verbose_name = 'Reservación'
        verbose_name_plural = 'Reservaciones'
        ordering = ['date', 'time']
        constraints = [
            models.UniqueConstraint(
                fields=['date', 'time', 'table'],
                condition=models.Q(status=ReservationStatus.CONFIRMED),
                name='unique_confirmed_reservation'
            )
        ]

    def __str__(self):
        return f"{self.customer_name} - {self.date} {self.time} ({self.get_status_display()})"

    def clean(self):
        super().clean()
        
        # Validación de fecha no pasada
        if self.date and self.date < timezone.now().date():
            raise ValidationError({'date': 'No se pueden hacer reservaciones para fechas pasadas.'})

        # Validación de horario comercial (8:00 AM - 11:00 PM)
        if self.time:
            opening_time = time(8, 0)
            closing_time = time(23, 0)
            if not (opening_time <= self.time <= closing_time):
                raise ValidationError(
                    {'time': 'El horario debe estar entre 8:00 AM y 11:00 PM.'}
                )

        # Validación de número de invitados
        if self.guests and self.guests < 1:
            raise ValidationError(
                {'guests': 'Debe haber al menos 1 persona en la reservación.'}
            )

        # Validación de disponibilidad de mesa
        if self.status == ReservationStatus.CONFIRMED and self.table and self.date and self.time:
            conflicting = Reservation.objects.filter(
                date=self.date,
                time=self.time,
                table=self.table,
                status=ReservationStatus.CONFIRMED
            ).exclude(pk=self.pk)
            
            if conflicting.exists():
                raise ValidationError(
                    {'table': 'Esta mesa ya está reservada para la fecha y hora seleccionada.'}
                )

    def save(self, *args, **kwargs):
        self.full_clean()  # Ejecuta todas las validaciones antes de guardar
        return super().save(*args, **kwargs)
