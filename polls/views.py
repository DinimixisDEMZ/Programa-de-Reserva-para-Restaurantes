from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse


def index(request):
    return HttpResponse("Hola mundo, está es la entrada de encuestas. :D")
