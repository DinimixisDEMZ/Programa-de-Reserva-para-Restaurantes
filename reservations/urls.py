from django.urls import path

from reservations.views import CreateReservationView,ListReservationView, UpdateReservationView, DeleteReservationView, DetailReservationView,api_create_reservation,reservaciones_page, api_estado

app_name = 'reservations'

urlpatterns = [
    path('create/',CreateReservationView.as_view(),name='create'),
    path('list/',ListReservationView.as_view(),name='list'),
    path('update/<int:pk>',UpdateReservationView.as_view(), name='update'),
    path('delete/<int:pk>/',DeleteReservationView.as_view(), name='delete'),
    path('detail/<int:pk>/',DetailReservationView.as_view(), name='detail'),
    path('api/reservar/', api_create_reservation, name='api_create_reservation'),
    path('reservaciones/', reservaciones_page, name='reservaciones_page'),
    path('api/estado/', api_estado, name='api_estado'),
]
