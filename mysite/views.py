from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views import generic

class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')  # Redirige a login después del registro
    template_name = 'signup.html'

    def form_valid(self, form):
        # Guarda el usuario primero
        response = super().form_valid(form)
        
        # Autentica al usuario automáticamente después del registro
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        
        if user is not None:
            login(self.request, user)
        
        return response

def main(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, "index.html", {})

def tables(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, "droga2.html", {})
