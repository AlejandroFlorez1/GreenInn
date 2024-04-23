from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, authenticate, login
from .models import Reserva
import json
from datetime import timedelta 
from django.utils.html import escapejs
# Create your views here.


def login_view(request):
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            User = authenticate(request, username=username, password=password)
            if User is not None:
                login(request, User)
                return redirect('inicio')
        return render(request, 'Core/login.html')

def home(request):
    return render(request, 'Core/principalHome.html')

def exit(request):
    logout(request)
    return redirect('home')

def Acercade(request):
    return render (request, 'Core/acercaDeHome.html')

def Cabañas(request):
    return render (request, 'Core/cabañasHome.html')

def Restaurante(request):
    return render (request, 'Core/restauranteHome.html')

@login_required
def inicio(request):
    return render (request, 'Core/baseUser.html')

def User_Reservas(request):
    return render (request, 'Core/UserReservas.html')

def User_Historial_Reservas(request):
    reservas = Reserva.objects.filter(usuario=request.user)
    return render (request, 'Core/UserHistorialReservas.html', {'reservas': reservas})

def User_Hacer_Reserva(request):
    reservas = Reserva.objects.filter(id=1)
    fechas_disponibles = []

    for reserva in reservas:
        rango_fechas = range((reserva.fechaCheckIn - timedelta(days=1)).day, reserva.fechaCheckOut.day + 1)
        mes_reserva = reserva.fechaCheckIn.strftime('%B') 
        fechas_disponibles.extend([(dia, mes_reserva) for dia in rango_fechas])

    fechas_disponibles = set(fechas_disponibles)
    fechas_disponibles = sorted(fechas_disponibles)
    fechas_disponibles_json = escapejs(json.dumps(fechas_disponibles))
    
    return render(request, 'Core/UserHacerReserva.html', {'fechas_disponibles_json': fechas_disponibles_json})
