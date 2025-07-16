from django.urls import path
from tables.views import CreateTableView

app_name = 'tables'

urlpatterns = [
    path('create/',CreateTableView.as_view(),name='create')
]