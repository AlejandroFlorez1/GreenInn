from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, authenticate, login
from .models import Reserva
from accounts.models import Profile
import json
from django.utils.html import escapejs
# Create your views here.


def login_view(request):
    if request.method == 'POST':
        form = request.POST.get('form')
        if form == 'login':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user_log = authenticate(request, username=username, password=password)
            if user_log is not None:
                login(request, user_log)
                return redirect('inicio')
            else:
                return HttpResponse('Usuario o contraseña incorrectos')
        elif form == 'registro':
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password1')
            password2 = request.POST.get('password2')
            if password == password2:
                # Crear un nuevo usuario
                new_user = User.objects.create_user(username, email, password)
                login(request, new_user)
                return redirect('inicio')
            else:
                error_message = 'Las contraseñas no coinciden'
                return render(request, 'Core/login.html', {'error_message': error_message})
    else:
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
    user_log = request.user
    profile = Profile.objects.get(user=user_log)

    contexto = {
        'profile': profile,
        'user': user_log,
    }
    return render (request, 'Core/UserInicio.html', contexto)

def User_Reservas(request):
    return render (request, 'Core/UserReservas.html')

def User_Historial_Reservas(request):
    reservas = Reserva.objects.filter(usuario=request.user)
    return render (request, 'Core/UserHistorialReservas.html', {'reservas': reservas})

def User_Hacer_Reserva(request):
    profile = Profile.objects.get(user=request.user)
    reservas = Reserva.objects.filter(id=1)
    fechas_disponibles = []

    for reserva in reservas:
        rango_fechas = range(reserva.fechaCheckIn.day, reserva.fechaCheckOut.day + 1)
        mes_reserva = reserva.fechaCheckIn.strftime('%m') 
        fechas_disponibles.extend([(dia, mes_reserva) for dia in rango_fechas])

    fechas_disponibles = set(fechas_disponibles)
    fechas_disponibles = sorted(fechas_disponibles)
    fechas_disponibles_json = escapejs(json.dumps(fechas_disponibles))
    
    return render(request, 'Core/UserHacerReserva.html', {'fechas_disponibles_json': fechas_disponibles_json, 'profile': profile})

def User_Profile(request):
    user_log = request.user
    profile = Profile.objects.get(user=user_log)
    return render (request, 'Core/UserPerfil.html', {'profile': profile})
