from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
# Create your views here.

@login_required
def reserva(request):
    return render(request, 'Core/reserva.html', {'form': UserCreationForm})

def login(request):
    return render(request, 'registration/login.html', {'form': UserCreationForm})

def home(request):
<<<<<<< Updated upstream
    return render(request, 'Core/prueba.html', {'form': UserCreationForm})
=======
    return render(request, 'Core/principalHome.html', {'form': UserCreationForm})
>>>>>>> Stashed changes

def exit(request):
    logout(request)
    return redirect('home')

def Acercade(request):
    return render (request, 'Core/acercaDeHome.html')

def Cabañas(request):
    return render (request, 'Core/cabañasHome.html')

def Restaurante(request):
    return render (request, 'Core/restauranteHome.html')
