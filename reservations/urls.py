from django.urls import path

from reservations.views import CreateReservationView,ListReservationView, api_create_reservation,reservaciones_page, api_estado

app_name = 'reservations'

urlpatterns = [
    path('create/',CreateReservationView.as_view(),name='create'),
    path('list/',ListReservationView.as_view(),name='list'),
    path('api/reservar/', api_create_reservation, name='api_create_reservation'),
    path('reservaciones/', reservaciones_page, name='reservaciones_page'),
    path('api/estado/', api_estado, name='api_estado'),
]
