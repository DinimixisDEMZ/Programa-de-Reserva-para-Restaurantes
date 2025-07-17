from django.shortcuts import render
from django.urls import reverse_lazy
from tables.models import Table
from tables.forms import TableForm
from django.views import generic
# Create your views here.


class CreateTableView(
    generic.CreateView
):
    queryset = Table.objects.all()
    form_class = TableForm
    template_name = 'tables/create-table.html'
    success_url = reverse_lazy('tables:create')

class UpdateTableView(
    generic.UpdateView
):
    queryset = Table.objects.all()
    form_class = TableForm
    template_name = 'tables/update-table.html'
    success_url = reverse_lazy('tables:update')
    

class DeleteTableView(
    generic.DeleteView
):
    queryset = Table.objects.all()
    success_url = reverse_lazy('tables:list')
    

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