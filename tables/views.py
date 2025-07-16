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