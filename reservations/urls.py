from django.urls import path
from .views import api_create_reservation,reservaciones_page, api_estado

urlpatterns = [
    path('api/reservar/', api_create_reservation, name='api_create_reservation'),
    path('reservaciones/', reservaciones_page, name='reservaciones_page'),
    path('api/estado/', api_estado, name='api_estado'),
]
