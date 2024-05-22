from django.contrib.auth.models import User, Group
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, authenticate, login
from .models import Reserva, Producto, Pedido_Producto
from accounts.models import Profile
from .models import Cabaña, Pedido, Pedido_Producto, Factura, Metodo_Pago, Estado
import json
from django.utils.html import escapejs
from datetime import datetime
from django.utils import timezone
from .decorators import login_required
from django.urls import reverse
from django.views.generic import ListView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .forms import ProductoForm, ProfileForm, UserForm, RegisterForm, CabañaForm

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
                if user_log.groups.filter(name='adminSystem').exists():
                    return redirect(reverse('admin:index'))
                elif user_log.groups.filter(name='Recepcionista').exists():
                    return redirect('inicioRecepcionista')
                elif user_log.groups.filter(name='usuario').exists():
                    return redirect('inicio')
                elif user_log.groups.filter(name='administrativo').exists():
                    return redirect('inicioAdministrativo')
                else:
                    return HttpResponse('No se encontró un grupo válido para el usuario')
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
    Reservas = Reserva.objects.filter(usuario=user_log)
    contexto = {
        'profile': profile,
        'user': user_log,
        'reservas': Reservas
    }
    return render (request, 'Core/UserInicio.html', contexto)

@login_required
def User_Reservas(request):
    return render (request, 'Core/UserReservas.html')

@login_required
def User_Historial_Reservas(request):
    reservas = Reserva.objects.filter(usuario=request.user, estado__in=[3, 9])
    user_log = request.user
    profile = Profile.objects.get(user=user_log)
    return render (request, 'Core/UserHistorialReservas.html', {'reservas': reservas, 'profile': profile})

@login_required
def User_Hacer_Reserva(request):
    if request.method == 'POST':        
        form = request.POST.get('form')
        if form == 'Buscar':
            cabañas = Cabaña.objects.all()
            id_cabaña = request.POST.get('cabaña')   
            profile = Profile.objects.get(user=request.user)
            reservas = Reserva.objects.filter(id=id_cabaña, estado__in=[3 , 9] )
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
            reser = Reserva.objects.filter(cabana=id_cabaña, estado__in=[3, 9])
            for reserva in reser:
                if fechaEntrada >= reserva.fechaCheckIn and fechaEntrada <= reserva.fechaCheckOut or fechaSalida >= reserva.fechaCheckIn and fechaSalida <= reserva.fechaCheckOut:
                    disponible = False
                    print("No disponible")
                    break
            
            datos = {
                'reservas': reser,
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
            total_factura = request.POST.get('total')
            if total_factura is not None:
                try:
                    total_factura = total_factura.replace(',', '.')
                    total_factura = float(total_factura)
                except ValueError:
                    # Maneja el error si la conversión falla
                    return HttpResponse("Error: El valor de 'total' no es un número flotante válido", status=400)
            else:
                total_factura = 0.0
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
            id_reserva = reserva.id
            reservafactura = Reserva.objects.get(id=id_reserva)
            metodo_pago = Metodo_Pago.objects.get(id=1)
            factura = Factura.objects.create(
                Reserva=reservafactura,
                metodo=metodo_pago,  # Aquí debes proporcionar el método de pago deseado
                Estado=Estado.objects.get(id=8),  # Aquí debes proporcionar el estado de la factura deseado
                total=total_factura  # Aquí debes proporcionar el total de la factura
)
            user_log = request.user
            profile = Profile.objects.get(user=user_log)
            fechas_disponibles = []
            fechas_disponibles = set(fechas_disponibles)
            fechas_disponibles = sorted(fechas_disponibles)
            fechas_disponibles_json = escapejs(json.dumps(fechas_disponibles)) 
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
    user_log = request.user
    profile = Profile.objects.get(user=user_log)
    if request.method == 'POST':
        if 'action' in request.POST:
            if request.POST['action'] == 'pagar':
                return redirect('pago', id_reserva=id_reserva)
            elif request.POST['action'] == 'hacer_pedido':
                reserva=Reserva.objects.get(id=id_reserva)
                estado_id = 5 #En carrito
                nuevo_pedido = Pedido.objects.create(Reserva=reserva, estado_id=estado_id)
                id_nuevo_pedido = nuevo_pedido.id
                nuevo_pedido.save()
                return redirect('hacerpedido', id_pedido=id_nuevo_pedido)
    else:
        reserva = get_object_or_404(Reserva, pk=id_reserva)
        id_estado = reserva.estado_id
    # Obtener los IDs de los pedidos en el estado 6
        pedidos_ids = Pedido.objects.filter(Reserva=reserva, estado_id=6).values_list('id', flat=True)
        factura = Factura.objects.filter(Reserva=reserva).first()
    # Obtener los productos asociados a los pedidos en el estado 6
        pedidos_productos = Pedido_Producto.objects.filter(pedido_id__in=pedidos_ids)
        productos_por_pedido = {}
        totalPagar = 0.0
        totalPagar+=factura.total

    # Llenar el diccionario con los productos por pedido
    for pedido_producto in pedidos_productos:
        pedido = pedido_producto.pedido
        producto = pedido_producto.producto
        if pedido not in productos_por_pedido:
            productos_por_pedido[pedido] = []
        productos_por_pedido[pedido].append(producto)
        totalPagar+=producto.precio

    return render(request, 'Core/UserDetalleReserva.html', {'reserva': reserva, 'productos_por_pedido': productos_por_pedido, 'factura': factura, 'totalPagar': totalPagar, 'id_estado': id_estado , 'profile': profile})

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

def Productos_Desayuno(request, id_pedido):
    if request.method == 'POST':
        if 'action' in request.POST:
            if request.POST['action'] == 'agregar':
                id_producto = request.POST.get('id') 
                cantidad = request.POST.get('cantidad')
                try:
                    cantidad = int(cantidad)
                except ValueError:
                    messages.error(request, 'El valor de la cantidad debe ser un número')
                    return redirect('tienda', id_pedido=id_pedido)
                
                nuevoPedido = Pedido_Producto.objects.create(producto_id=id_producto, pedido_id=id_pedido, cantidad=cantidad)
                nuevoPedido.save()
                return redirect('productosDesayuno', id_pedido=id_pedido)
    else:
        productos=Producto.objects.all()
        productos_=Pedido_Producto.objects.filter(pedido_id=id_pedido)
        total= productos_.count()
        return render(request, 'Core/tienda/productosDesayuno.html', {'productos': productos, 'total': total, 'id_pedido': id_pedido})


def Productos_almuerzo(request, id_pedido):
    if request.method == 'POST':
        if 'action' in request.POST:
            if request.POST['action'] == 'agregar':
                id_producto = request.POST.get('id') 
                cantidad = request.POST.get('cantidad')
                try:
                    cantidad = int(cantidad)
                except ValueError:
                    messages.error(request, 'El valor de la cantidad debe ser un número')
                    return redirect('tienda', id_pedido=id_pedido)
                
                nuevoPedido = Pedido_Producto.objects.create(producto_id=id_producto, pedido_id=id_pedido, cantidad=cantidad)
                nuevoPedido.save()
                return redirect('productosAlmuerzo', id_pedido=id_pedido)
    else:
        productos=Producto.objects.all()
        productos_=Pedido_Producto.objects.filter(pedido_id=id_pedido)
        total= productos_.count()
        return render(request, 'Core/tienda/productosAlmuerzo.html', {'productos': productos, 'total': total, 'id_pedido': id_pedido})

def Productos_comida_rapida(request, id_pedido):
    if request.method == 'POST':
        if 'action' in request.POST:
            if request.POST['action'] == 'agregar':
                id_producto = request.POST.get('id') 
                cantidad = request.POST.get('cantidad')
                try:
                    cantidad = int(cantidad)
                except ValueError:
                    messages.error(request, 'El valor de la cantidad debe ser un número')
                    return redirect('tienda', id_pedido=id_pedido)
                
                nuevoPedido = Pedido_Producto.objects.create(producto_id=id_producto, pedido_id=id_pedido, cantidad=cantidad)
                nuevoPedido.save()
                return redirect('productosComidasRapidas', id_pedido=id_pedido)
    else:
        productos=Producto.objects.all()
        productos_=Pedido_Producto.objects.filter(pedido_id=id_pedido)
        total= productos_.count()
        return render(request, 'Core/tienda/productosComidaRapida.html', {'productos': productos, 'total': total, 'id_pedido': id_pedido})

def Productos_bebidas(request, id_pedido):
    if request.method == 'POST':
        if 'action' in request.POST:
            if request.POST['action'] == 'agregar':
                id_producto = request.POST.get('id') 
                cantidad = request.POST.get('cantidad')
                try:
                    cantidad = int(cantidad)
                except ValueError:
                    messages.error(request, 'El valor de la cantidad debe ser un número')
                    return redirect('tienda', id_pedido=id_pedido)
                
                nuevoPedido = Pedido_Producto.objects.create(producto_id=id_producto, pedido_id=id_pedido, cantidad=cantidad)
                nuevoPedido.save()
                return redirect('productosBebidas', id_pedido=id_pedido)
    else:
        productos=Producto.objects.all()
        productos_=Pedido_Producto.objects.filter(pedido_id=id_pedido)
        total= productos_.count()
        return render(request, 'Core/tienda/productosBebidas.html', {'productos': productos, 'total': total, 'id_pedido': id_pedido})

def Productos_snacks(request, id_pedido):
    if request.method == 'POST':
        if 'action' in request.POST:
            if request.POST['action'] == 'agregar':
                id_producto = request.POST.get('id') 
                cantidad = request.POST.get('cantidad')
                try:
                    cantidad = int(cantidad)
                except ValueError:
                    messages.error(request, 'El valor de la cantidad debe ser un número')
                    return redirect('tienda', id_pedido=id_pedido)
                
                nuevoPedido = Pedido_Producto.objects.create(producto_id=id_producto, pedido_id=id_pedido, cantidad=cantidad)
                nuevoPedido.save()
                return redirect('productosSnacks', id_pedido=id_pedido)
    else:
        productos=Producto.objects.all()
        productos_=Pedido_Producto.objects.filter(pedido_id=id_pedido)
        total= productos_.count()
        return render(request, 'Core/tienda/productosSnacks.html', {'productos': productos, 'total': total, 'id_pedido': id_pedido})

def User_Hacer_Pedido (request, id_pedido):
    if request.method == 'POST':
        if 'action' in request.POST:
            if request.POST['action'] == 'agregar':
                id_producto = request.POST.get('id') 
                cantidad = request.POST.get('cantidad')
                try:
                    cantidad = int(cantidad)
                except ValueError:
                    messages.error(request, 'El valor de la cantidad debe ser un número')
                    return redirect('tienda', id_pedido=id_pedido)
                
                nuevoPedido = Pedido_Producto.objects.create(producto_id=id_producto, pedido_id=id_pedido, cantidad=cantidad)
                nuevoPedido.save()
                return redirect('hacerpedido', id_pedido=id_pedido)
    else:
        productos_=Pedido_Producto.objects.filter(pedido_id=id_pedido)
        total= productos_.count()
        productos=Producto.objects.all()
        return render(request, 'Core/tienda/productosTodos.html', {'id_pedido': id_pedido, 'productos': productos, 'total': total})
    
def Carrito(request, id_pedido):
    productos_=Pedido_Producto.objects.filter(pedido_id=id_pedido)
    totalProductos = []
    totalCosto = 0
    for producto in productos_:
        item = Producto.objects.get(id=producto.producto_id)
        id=producto.id
        subtotal=item.precio*item.cantidad
        producto_info = {
            'id': id,
            'producto': item,
            'subtotal': subtotal
        }
        totalCosto += item.precio
        totalProductos.append(producto_info)
    
    return render(request, 'Core/tienda/carrito_Pago.html', {'id_pedido': id_pedido, 'productos': totalProductos, 'total': totalCosto})

def vaciar_carrito(request, id_pedido):
    Pedido_Producto.objects.filter(pedido_id=id_pedido).delete()
    return redirect('carrito', id_pedido=id_pedido)

def Eliminar_elemento(request, id_pedido_producto):
    pedido_producto = get_object_or_404(Pedido_Producto, pk=id_pedido_producto)
    id_pedido = pedido_producto.pedido_id  # Obtenemos el id del pedido antes de eliminar el pedido_producto
    pedido_producto.delete()
    return redirect('carrito', id_pedido=id_pedido)

def Pedir(request, id_pedido):
    pedido = Pedido.objects.get(id=id_pedido)
    pedido.estado_id = 6

    pedido.save()
    id_reserva =pedido.Reserva.id
    return redirect('detalle_reserva' , id_reserva=id_reserva)

def Pago(request, id_reserva):  
    if request.method == 'POST':
        reserva = Reserva.objects.get(id=id_reserva)
        reserva.estado_id = 4
        reserva.save()
        return redirect('User_Historial_Reservas')
    else:  
        return render(request, 'Core/notFound.html', {'id_reserva': id_reserva})
    
def InicioRecepcionista(request):    
    user_log = request.user
    profile = Profile.objects.get(user=user_log)
    return render(request, 'Core/recepcionista/BaseRecepcionista.html', {'profile': profile, 'user': user_log})

def CheckIn(request):
    reservas = Reserva.objects.filter( estado__in=[3])
    return render(request, 'Core/recepcionista/recepcionistaCheckin.html', {'reservas': reservas})

def ValidarCheckIn(request, id_reserva):
    reserva = reserva = get_object_or_404(Reserva, pk=id_reserva)
    if request.method == 'POST':
        # Si se recibe una solicitud POST, eliminar la reserva
        reserva.estado_id = 9
        reserva.save()
        # Redirigir a alguna página después de la eliminación (por ejemplo, la página de inicio)
        return redirect('checkin')  # Ajusta 'inicio' según tu URL de inicio

    # Si no es una solicitud POST, renderizar un mensaje de error
    return render(request, 'Core/recepcionista/recepcionistaCheckin.html', {'mensaje': 'Solicitud no válida'})

def Historial(request):
    reservas = Reserva.objects.filter( estado__in=[4])
    user_log = request.user
    profile = Profile.objects.get(user=user_log)
    return render(request, 'Core/UserHistorial.html', {'reservas': reservas, 'profile': profile} )

class ProductoListView(ListView):
    model = Producto
    template_name = 'recepcionista/recepcionistaPedidos.html'
    context_object_name = 'productos'

class ProductoUpdateView(UpdateView):
    model = Producto
    form_class = ProductoForm
    template_name = 'reservas/recepcionistaCrear.html'
    success_url = reverse_lazy('producto_list')

class ProductoDeleteView(DeleteView):
    model = Producto
    template_name = 'reservas/producto_confirm_delete.html'
    success_url = reverse_lazy('producto_list')

def producto_create_view(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('producto_list')
    else:
        form = ProductoForm()
    return render(request, 'reservas/recepcionistaCrear.html', {'form': form})

def Pedidos(request):
    pedidos_Espera = Pedido.objects.select_related('Reserva__usuario', 'Reserva__cabana').filter(estado__in=[6])
    pedidos_Entregado = Pedido.objects.select_related('Reserva__usuario', 'Reserva__cabana').filter(estado__in=[7])
    return render(request, 'Core/recepcionista/recepcionistaPedidos.html', {
        'pedidos_espera': pedidos_Espera,
        'pedidos_entregado': pedidos_Entregado
    })

def Entregar_pedido(request, id_pedido):
    pedido = get_object_or_404(Pedido, pk=id_pedido)
    productos_pedido = Pedido_Producto.objects.filter(pedido=pedido)
    
    if request.method == "POST":

        # Aquí puedes actualizar el estado del pedido a "entregado"
        estado_entregado = Estado.objects.get(tipEstado="Entregado")  # Asegúrate de tener el estado "Entregado" en la base de datos
        pedido.estado = estado_entregado
        pedido.save()
        for item in productos_pedido:
            producto = item.producto
            try:
                producto.reducir_cantidad(item.cantidad)
            except ValueError as e:
                # Manejar el caso en el que no haya suficiente stock
                return render(request, 'Core/recepcionista/error.html', {'error': str(e)})
        return redirect('pedidos_view')  # Redirige a la lista de pedidos o a otra vista según tu necesidad

    return render(request, 'Core/recepcionista/entregar_pedido.html', {
        'pedido': pedido,
        'productos_pedido': productos_pedido
    })

def inicioAdmin (request):
    user_log = request.user
    profile = Profile.objects.get(user=user_log)
    return render(request, 'Core/admin/inicioAdmin.html', {'profile': profile, 'user': user_log})

def recepcionistas_view(request):
    recepcionistas_group = Group.objects.get(name='Recepcionista')
    recepcionistas = recepcionistas_group.user_set.all()
    return render(request, 'Core/admin/adminRecepcionistas.html', {'recepcionistas': recepcionistas})

def recepcionista_detail(request, username):
    user = get_object_or_404(User, username=username)
    profile = user.profile
    return render(request, 'recepcionistas/recepcionista_detail.html', {'user': user, 'profile': profile})

def recepcionista_edit(request, username):
    user = get_object_or_404(User, username=username)
    profile = user.profile
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('recepcionistas_view')
    else:
        user_form = UserForm(instance=user)
        profile_form = ProfileForm(instance=profile)
    return render(request, 'Core/admin/recepcionista_edit.html', {'user_form': user_form, 'profile_form': profile_form})

def recepcionista_create(request):
    if request.method == 'POST':
        user_form = RegisterForm(request.POST)
        profile_form = ProfileForm(request.POST, request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            try:
                profile = Profile.objects.get(user=user)
            except Profile.DoesNotExist:
                profile = profile_form.save(commit=False)
                profile.user = user
                profile.save()
            group = Group.objects.get(name='Recepcionista')
            user.groups.add(group)
            return redirect('recepcionista_view')
    else:
        user_form = UserForm()
        profile_form = ProfileForm()
    return render(request, 'Core/admin/adminRecepcionistaCrear.html', {'user_form': user_form, 'profile_form': profile_form})

def recepcionista_delete(request, username):
    user = get_object_or_404(User, username=username)
    user.delete()
    return redirect('recepcionista_view')

def cabañas_list(request):
    cabañas = Cabaña.objects.all()
    return render(request, 'Core/admin/cabañas_list.html', {'cabañas': cabañas})

def cabaña_create(request):
    if request.method == 'POST':
        form = CabañaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('cabañas_list')
    else:
        form = CabañaForm()
    return render(request, 'Core/admin/cabaña_form.html', {'form': form})

def cabaña_update(request, pk):
    cabaña = get_object_or_404(Cabaña, pk=pk)
    if request.method == 'POST':
        form = CabañaForm(request.POST, request.FILES, instance=cabaña)
        if form.is_valid():
            form.save()
            return redirect('cabañas_list')
    else:
        form = CabañaForm(instance=cabaña)
    return render(request, 'Core/admin/cabaña_form.html', {'form': form})

def cabaña_delete(request, pk):
    cabaña = get_object_or_404(Cabaña, pk=pk)
    if request.method == 'POST':
        cabaña.delete()
        return redirect('cabañas_list')
    return render(request, 'Core/admin/cabaña_confirm_delete.html', {'cabaña': cabaña})

def users_with_profiles(request):
    users_with_profiles = User.objects.select_related('profile').all()
    return render(request, 'Core/admin/users_with_profiles.html', {'users_with_profiles': users_with_profiles})