from django.urls import path
from .views import (
    CreateReservationView,
    ListReservationView,
    UpdateReservationView,
    DeleteReservationView,
    DetailReservationView,
    api_create_reservation,
    reservaciones_dashboard,  # Nombre actualizado
    api_table_status  # Nombre actualizado
)

app_name = 'reservations'

urlpatterns = [
    # Vistas basadas en clase
    path('create/', CreateReservationView.as_view(), name='create'),
    path('list/', ListReservationView.as_view(), name='list'),
    path('update/<int:pk>/', UpdateReservationView.as_view(), name='update'),
    path('delete/<int:pk>/', DeleteReservationView.as_view(), name='delete'),
    path('detail/<int:pk>/', DetailReservationView.as_view(), name='detail'),
    
    # Vistas de API
    path('api/reservar/', api_create_reservation, name='api_create'),
    path('api/estado/', api_table_status, name='api_status'),  # Nombre actualizado
    
    # Vista de dashboard (nombre original conservado)
    path('reservaciones/', reservaciones_dashboard, name='dashboard'),
    
    # Redirección para mantener compatibilidad (opcional)
    path('old/reservaciones/', reservaciones_dashboard, name='reservaciones_page'),
]
