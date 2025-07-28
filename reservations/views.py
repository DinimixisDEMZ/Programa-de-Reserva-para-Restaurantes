# reservations/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.views import generic
from django.db import transaction
import json
from datetime import date
from .models import Reservation, ReservationStatus
from tables.models import Table, TableStatus
from .forms import ReservationForm

class ReservationBaseView:
    model = Reservation
    form_class = ReservationForm
    success_url = reverse_lazy('reservations:list')

class CreateReservationView(ReservationBaseView, generic.CreateView):
    template_name = 'reservations/create-reservation.html'
    
    def form_valid(self, form):
        """Guarda la reserva y actualiza el estado de la mesa"""
        with transaction.atomic():
            response = super().form_valid(form)
            self.object.table.status = TableStatus.RESERVED
            self.object.table.save()
        return response

class ListReservationView(ReservationBaseView, generic.ListView):
    template_name = 'reservations/list.html'
    context_object_name = 'reservations'
    paginate_by = 10
    
    def get_queryset(self):
        return Reservation.objects.filter(date__gte=date.today()).order_by('date', 'time')

class UpdateReservationView(ReservationBaseView, generic.UpdateView):
    template_name = 'reservations/update.html'
    
    def form_valid(self, form):
        """Maneja cambios de mesa en actualizaciones"""
        old_table = self.get_object().table
        with transaction.atomic():
            response = super().form_valid(form)
            # Liberar mesa anterior si cambió
            if old_table != self.object.table:
                old_table.status = TableStatus.FREE
                old_table.save()
            self.object.table.status = TableStatus.RESERVED
            self.object.table.save()
        return response

# Tu vista DeleteReservationView existente
class DeleteReservationView(ReservationBaseView, generic.DeleteView):
    template_name = 'reservations/confirm-delete.html'  # Añadido template para confirmación
    
    def get_success_url(self):
        # Redirige a la lista de reservaciones para eliminar después de una eliminación exitosa
        return reverse_lazy('reservation_list_to_delete') # Usamos reverse_lazy para la URL de la lista de eliminación

    def delete(self, request, *args, **kwargs):
        """Libera la mesa al cancelar reserva"""
        with transaction.atomic():
            reservation = self.get_object()
            reservation.table.status = TableStatus.FREE
            reservation.table.save()
            return super().delete(request, *args, **kwargs)

class DetailReservationView(ReservationBaseView, generic.DetailView):
    template_name = 'reservations/detail.html'

@csrf_exempt
def api_create_reservation(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            with transaction.atomic():
                table = Table.objects.get(id=data['tableId'])
                reservation = Reservation.objects.create(
                    customer_name=data['customerName'],
                    customer_phone=data['customerPhone'],
                    customer_email=data['customerEmail'],
                    date=data['date'],
                    time=data['time'],
                    guests=data['guests'],
                    notes=data['notes'],
                    table=table,
                    status=ReservationStatus.CONFIRMED
                )
                table.status = TableStatus.RESERVED
                table.save()
                return JsonResponse({
                    'success': True,
                    'reservationId': reservation.id
                })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=400)
    return JsonResponse({'error': 'Método no permitido'}, status=405)

def reservaciones_dashboard(request):
    """Vista consolidada para el panel de reservas"""
    context = {
        'tables': Table.objects.all().order_by('number'),
        'reservations_today': Reservation.objects.filter(date=date.today()).order_by('time'),
        'upcoming_reservations': Reservation.objects.filter(date__gt=date.today()).order_by('date', 'time')[:5],
        'reservation_statuses': ReservationStatus.choices,
        'table_statuses': TableStatus.choices
    }
    return render(request, 'reservations/dashboard.html', context)

def api_table_status(request):
    """Endpoint para estado de mesas (AJAX)"""
    tables = Table.objects.all().values('id', 'number', 'number_of_chairs', 'location', 'status').order_by('number')
    reservations = Reservation.objects.filter(date=date.today()).values(
        'id', 'table_id', 'time', 'customer_name', 'guests', 'status'
    ).order_by('time')
    return JsonResponse({
        'tables': list(tables),
        'reservations': list(reservations),
        'current_date': date.today().isoformat()
    })

# Nueva vista para listar las reservaciones que se pueden eliminar
class ReservationListToDeleteView(generic.ListView):
    model = Reservation
    template_name = 'reservations/reservation_list_to_delete.html'
    context_object_name = 'reservations' # Nombre de la lista de objetos en el contexto
    
    def get_queryset(self):
        # En un escenario real, aquí filtrarías las reservaciones por el usuario actual.
        # Por ejemplo: return Reservation.objects.filter(customer_email=self.request.user.email).order_by('date', 'time')
        return Reservation.objects.all().order_by('date', 'time') # Para este ejemplo, listamos todas

# Versiones compatibles (pueden eliminarse si no se necesitan)
def reservaciones_page(request):
    """Alias para mantener compatibilidad"""
    return reservaciones_dashboard(request)

def api_estado(request):
    """Alias para mantener compatibilidad con código existente"""
    return api_table_status(request)
