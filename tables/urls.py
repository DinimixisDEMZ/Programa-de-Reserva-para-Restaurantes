from django.urls import path
from tables.views import CreateTableView, UpdateTableView, DetailTableView, ListTableView, DeleteTableView

app_name = 'tables'

urlpatterns = [
    path('create/',CreateTableView.as_view(),name='create'),
    path('update/<int:pk>/',UpdateTableView.as_view(), name='update'),
    path('delete/<int:pk>/',DeleteTableView.as_view(), name='delete'),
    path('detail/<int:pk>/',DetailTableView.as_view(), name='detail'),
    path('list/', ListTableView.as_view(), name='list')
]