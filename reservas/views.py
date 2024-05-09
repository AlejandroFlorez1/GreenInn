from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, authenticate, login
from .models import Reserva
from accounts.models import Profile
from .models import Cabaña
import json
from django.utils.html import escapejs
from datetime import datetime
from django.utils import timezone

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
    user_log = request.user
    profile = Profile.objects.get(user=user_log)
    return render (request, 'Core/UserHistorialReservas.html', {'reservas': reservas, 'profile': profile})

def User_Hacer_Reserva(request):
    if request.method == 'POST':        
        form = request.POST.get('form')
        if form == 'Buscar':
            cabañas = Cabaña.objects.all()
            id_cabaña = request.POST.get('cabaña')   
            profile = Profile.objects.get(user=request.user)
            reservas = Reserva.objects.filter(id=id_cabaña)
            fechas_disponibles = []
            fechas={}
            fechaEntrada_str = request.POST.get('dateEntrada')
            fechaSalida_str = request.POST.get('dateSalida')
            if fechaEntrada_str and fechaSalida_str:
                fechaEntrada = datetime.strptime(fechaEntrada_str, '%Y-%m-%d').date()
                fechaSalida = datetime.strptime(fechaSalida_str, '%Y-%m-%d').date()

                # Formatear las fechas según el formato YYYY-MM-DD
                fechaEntrada_fmt = fechaEntrada.strftime('%Y-%m-%d')
                fechaSalida_fmt = fechaSalida.strftime('%Y-%m-%d')
                fechas={
                    'fechaEntrada': fechaEntrada_fmt,
                    'fechaSalida': fechaSalida_fmt
                }

            for reserva in reservas:
                rango_fechas = range(reserva.fechaCheckIn.day, reserva.fechaCheckOut.day + 1)
                mes_reserva = reserva.fechaCheckIn.strftime('%m') 
                fechas_disponibles.extend([(dia, mes_reserva) for dia in rango_fechas])

            fechas_disponibles = set(fechas_disponibles)
            fechas_disponibles = sorted(fechas_disponibles)
            fechas_disponibles_json = escapejs(json.dumps(fechas_disponibles))

            diferencia_dias = (fechaSalida - fechaEntrada).days
            numPersonas_srt = request.POST.get('numPersonas')
            numPersonas = int(numPersonas_srt)
            cabaña = Cabaña.objects.get(pk=id_cabaña)

            precioCabaña = cabaña.precio
            subtotal = (numPersonas * 50000) + precioCabaña*diferencia_dias
            total = subtotal*0.19 + subtotal
            disponible = True;
            for reserva in reservas:
                if reserva.fechaCheckIn <= fechaEntrada < reserva.fechaCheckOut or reserva.fechaCheckIn <= fechaSalida < reserva.fechaCheckOut:
                    disponible = False
                    print("No disponible")
                    break
            
            datos = {
                'numPersonas': numPersonas,
                'cabaña': cabaña,
                'subtotal': subtotal,
                'total': total,
                'disponible': disponible,
                'id_cabaña': id_cabaña
            }
            
            return render(request, 'Core/UserHacerReserva.html', {'fechas_disponibles_json': fechas_disponibles_json, 'profile': profile, 'cabañas': cabañas, 'fechas': fechas, 'datos': datos}, )
        elif form=='Reservar':
            estado_id = 3 #Activo
            cabana_id = request.POST.get('id_cabaña')
            usuario_id = request.user.id  # Suponiendo que estás autenticando usuarios
            fecha_reserva = timezone.now().date()  # Fecha actual
            fecha_check_in = request.POST.get('FecEntrada')
            fecha_check_out = request.POST.get('FecSalida')
            num_personas = request.POST.get('NumPersonas')

            reserva = Reserva(
                estado_id=estado_id,
                cabana_id=cabana_id,
                usuario_id=usuario_id,
                fechaReserva=fecha_reserva,
                fechaCheckIn=fecha_check_in,
                fechaCheckOut=fecha_check_out,
                numPersonas=num_personas
            )
            reserva.save()
            user_log = request.user
            profile = Profile.objects.get(user=user_log)
            return render(request, 'Core/UserInicio.html', {'profile': profile})    
        else:
            fechas_disponibles = []
            fechas_disponibles = set(fechas_disponibles)
            fechas_disponibles = sorted(fechas_disponibles)
            fechas_disponibles_json = escapejs(json.dumps(fechas_disponibles))   
            user_log = request.user
            profile = Profile.objects.get(user=user_log)
            cabañas = Cabaña.objects.all()
            return render(request, 'Core/UserHacerReserva.html', {'profile': profile, 'fechas_disponibles_json': fechas_disponibles_json, 'cabañas': cabañas})
    else:
        fechas_disponibles = []
        fechas_disponibles = set(fechas_disponibles)
        fechas_disponibles = sorted(fechas_disponibles)
        fechas_disponibles_json = escapejs(json.dumps(fechas_disponibles))   
        user_log = request.user
        profile = Profile.objects.get(user=user_log)
        cabañas = Cabaña.objects.all()
        return render(request, 'Core/UserHacerReserva.html', {'profile': profile, 'fechas_disponibles_json': fechas_disponibles_json, 'cabañas': cabañas})

def User_Profile(request):
    if request.method == 'POST':
        user_log = request.user
        profile = Profile.objects.get(user=user_log)
        nombre = request.POST.get('first_name')
        apellido = request.POST.get('last_name')
        if nombre:
            user_log.first_name = nombre
        if apellido:
            user_log.last_name = apellido     
        profile.telephone = request.POST.get('telephone')
        profile.address = request.POST.get('address')
        image = request.FILES.get('imagen')
        if image:            
            profile.image = image
        user_log.save()
        profile.save()
        return render (request, 'Core/UserPerfil.html', {'profile': profile})
    else:
        user_log = request.user
        profile = Profile.objects.get(user=user_log)
        return render (request, 'Core/UserPerfil.html', {'profile': profile})
    
def User_Detalle_Reserva(request, id_reserva):
    reserva= get_object_or_404(Reserva, pk=id_reserva)
    return render(request, 'PagosProductos/main_Pago.html', {'reserva': reserva})

def User_Eliminar_Reserva(request, reserva_id):
    # Obtener la reserva por su ID
    reserva = get_object_or_404(Reserva, pk=reserva_id)
    
    if request.method == 'POST':
        # Si se recibe una solicitud POST, eliminar la reserva
        reserva.delete()
        # Redirigir a alguna página después de la eliminación (por ejemplo, la página de inicio)
        return redirect('User_Historial_Reservas')  # Ajusta 'inicio' según tu URL de inicio

    # Si no es una solicitud POST, renderizar un mensaje de error
    return render(request, 'Core/UserHistorialReservas.html', {'mensaje': 'Solicitud no válida'})