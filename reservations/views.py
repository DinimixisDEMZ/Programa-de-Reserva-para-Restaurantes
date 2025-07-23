from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from .models import Reservation
from datetime import date
from tables.models import Table,TableStatus
from django.views import generic
from reservations.models import Reservation
from reservations.forms import ReservationForm


# Create your views here.

class CreateReservationView(
    generic.CreateView
):
    queryset = Reservation.objects.all()
    form_class = ReservationForm
    template_name = 'reservaciones/create-reservation.html'
    success_url = reverse_lazy('reservations:list')

class ListReservationView(
    generic.ListView
):
    queryset = Reservation.objects.all()
    context_object_name = 'reservations'
    template_name = 'reservaciones/list-reservation.html'
    
    def get_context_data(self, **kwargs):  
        context = super().get_context_data(**kwargs)
        context['form'] = ReservationForm()
        return context
    
    def post(self, request, *args, **kwargs):
        form = ReservationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('reservations:list')
        else:
            return self.render_to_response(self.get_context_data(form=form))


@csrf_exempt
def api_create_reservation(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            table = Table.objects.get(id=data['tableId'])

            Reservation.objects.create(
                customer_name=data['customerName'],
                customer_phone=data['customerPhone'],
                customer_email=data['customerEmail'],
                date=data['date'],
                time=data['time'],
                guests=data['guests'],
                notes=data['notes'],
                table=table,
                status='confirmed'
            )

            table.status = 2  # Cambia estado de la mesa
            table.save()

            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    # 👇 Esta es la solución para métodos que no son POST
    return JsonResponse({'error': 'Método no permitido'}, status=405)


def reservaciones_page(request):
    tables = [
        {
            'id': t.id,
            'number': t.id,  # usamos el ID como número visible
            'capacity': t.number_of_chairs,
            'location': t.location,
            'status': (
                'available' if t.status == TableStatus.FREE else
                'occupied' if t.status == TableStatus.OCCUPIED else
                'reserved'
            )
        }
        for t in Table.objects.all()
    ]

    reservations = list(Reservation.objects.filter(date=date.today()).values(
        'id', 'table_id', 'customer_name', 'customer_phone',
        'customer_email', 'date', 'time', 'guests', 'status', 'notes'
    ))

    return render(request, 'reservaciones/reserva.html', {
        'tables_data': tables,
        'reservations_data': reservations
    })

def api_estado(request):
    tables = [
        {
            'id': t.id,
            'number': t.id,  # Si tienes un campo específico de número, puedes usarlo
            'capacity': t.number_of_chairs,
            'location': t.location,
            'status': (
                'available' if t.status == TableStatus.FREE else
                'occupied' if t.status == TableStatus.OCCUPIED else
                'reserved'
            )
        }
        for t in Table.objects.all()
    ]

    reservations = list(Reservation.objects.filter(date=date.today()).values(
        'id', 'table_id', 'customer_name', 'customer_phone',
        'customer_email', 'date', 'time', 'guests', 'status', 'notes'
    ))

    return JsonResponse({
        'tables': tables,
        'reservations': reservations
    })