# mi_aplicacion/views.py
from django.shortcuts import render

def menu_principal_view(request):
    return render(request, 'menu/Menu.html')