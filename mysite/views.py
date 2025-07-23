from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

def main(request):
    return render(request, "index.html", {})

def tables(request):
    return render(request, "droga2.html", {})
