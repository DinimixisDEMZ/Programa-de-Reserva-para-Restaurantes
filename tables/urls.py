from django.urls import path
from tables.views import CreateTableView, UpdateTableView, DetailTableView, ListTableView, DeleteTableView

app_name = 'tables' # Mantener el app_name para namespacing

urlpatterns = [
    path('create/', CreateTableView.as_view(), name='create_table'), # Nombre actualizado
    path('update/<int:pk>/', UpdateTableView.as_view(), name='update_table'), # Nombre actualizado
    path('delete/<int:pk>/', DeleteTableView.as_view(), name='confirm_delete_table'), # Nombre actualizado para confirmación
    path('detail/<int:pk>/', DetailTableView.as_view(), name='detail_table'), # Nombre actualizado
    path('list/', ListTableView.as_view(), name='list_tables') # Nombre actualizado
]
