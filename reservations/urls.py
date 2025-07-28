# reservations/urls.py

from django.urls import path
# Importa las vistas que usarás
from .views import (
    DeleteReservationView,
    ReservationListToDeleteView,
    CreateReservationView,
    ListReservationView,
    UpdateReservationView,
    DetailReservationView,
    api_create_reservation,
    reservaciones_dashboard,
    api_table_status,
    reservaciones_page,
    api_estado
)

app_name = 'reservations' # Vuelve a añadir el app_name para namespacing

urlpatterns = [
    # Vistas basadas en clase
    path('create/', CreateReservationView.as_view(), name='create_reservation'),
    path('list/', ListReservationView.as_view(), name='list_reservations'), # Renombrado para consistencia
    path('update/<int:pk>/', UpdateReservationView.as_view(), name='update_reservation'),
    path('detail/<int:pk>/', DetailReservationView.as_view(), name='detail_reservation'),
    
    # Vistas de API
    path('api/create/', api_create_reservation, name='api_create_reservation'), # Ajustado a tu convención
    path('api/table-status/', api_table_status, name='api_table_status'), # Ajustado a tu convención
    
    # Vista de dashboard
    path('dashboard/', reservaciones_dashboard, name='dashboard'),
    
    # URLs para la funcionalidad de eliminación interactiva
    path('delete/', ReservationListToDeleteView.as_view(), name='list_to_delete'), # Renombrado para consistencia
    path('<int:pk>/confirm-delete/', DeleteReservationView.as_view(), name='confirm_delete'), # Renombrado para consistencia
    
    # Redirecciones para mantener compatibilidad (opcional)
    path('old/reservaciones/', reservaciones_dashboard, name='reservaciones_page'),
    path('api_estado/', api_estado, name='api_estado'),
]
