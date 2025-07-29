from django.shortcuts import render
from django.urls import reverse_lazy
from tables.models import Table # Asegúrate de que Table y TableStatus estén definidos en tables/models.py
from tables.forms import TableForm # Asumiendo que tienes un forms.py para TableForm
from django.views import generic
from django.db import transaction # Importar transaction

# Create your views here.

class CreateTableView(
    generic.CreateView
):
    queryset = Table.objects.all()
    form_class = TableForm
    template_name = 'tables/create-table.html'
    success_url = reverse_lazy('tables:list_tables') # Apunta a la lista de tablas

class UpdateTableView(
    generic.UpdateView
):
    queryset = Table.objects.all()
    form_class = TableForm
    template_name = 'tables/update-table.html'
    success_url = reverse_lazy('tables:list_tables') # Apunta a la lista de tablas
    

class DeleteTableView(
    generic.DeleteView
):
    queryset = Table.objects.all()
    template_name = 'tables/table_confirm_delete.html' # Usa la plantilla de confirmación
    success_url = reverse_lazy('tables:list_tables') # Redirige a la lista de tablas después de eliminar
    
    # Puedes añadir lógica adicional aquí si es necesario antes de la eliminación.
    # Por ejemplo, si necesitas cambiar el estado de alguna reservación asociada, etc.
    # def delete(self, request, *args, **kwargs):
    #     with transaction.atomic():
    #         table = self.get_object()
    #         # Lógica adicional aquí, si es necesario
    #         return super().delete(request, *args, **kwargs)


class DetailTableView(
    generic.DetailView
):
    queryset = Table.objects.all()
    template_name = 'tables/detail-table.html'

class ListTableView(
    generic.ListView
):
    queryset = Table.objects.all()
    context_object_name = 'tables'
    template_name = 'tables/list-table.html'
