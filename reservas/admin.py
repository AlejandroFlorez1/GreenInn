from django.contrib import admin
from .models import Categoria, Estado, Cabaña, Reserva, Pedido, Producto, Pedido_Producto, Metodo_Pago, Factura

# Register your models here.
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nomCategoria',)

admin.site.register(Categoria, CategoriaAdmin)

class EstadoAdmin(admin.ModelAdmin):
    list_display = ('tipEstado',)

admin.site.register(Estado, EstadoAdmin)

class CabañaAdmin(admin.ModelAdmin):
    list_display = ( 'id','nomCabaña', 'perMax', 'precio', 'descripcion', 'imagen')

admin.site.register(Cabaña, CabañaAdmin)

class ReservaAdmin(admin.ModelAdmin):
    list_display = ('estado', 'cabana', 'usuario', 'fechaReserva', 'fechaCheckIn', 'fechaCheckOut')

admin.site.register(Reserva, ReservaAdmin)

class PedidoAdmin(admin.ModelAdmin):
    list_display = ('Reserva', 'estado')

admin.site.register(Pedido, PedidoAdmin)

class ProductoAdmin(admin.ModelAdmin):
    list_display = ('categoria', 'Estado', 'nomProducto', 'precio', 'descripcion', 'cantidad')

admin.site.register(Producto, ProductoAdmin)

class Pedido_ProductoAdmin(admin.ModelAdmin):
    list_display = ('pedido', 'producto')

admin.site.register(Pedido_Producto, Pedido_ProductoAdmin)

class metodoPagoAdmin(admin.ModelAdmin):
    list_display = ('nomMetodo',)

admin.site.register(Metodo_Pago, metodoPagoAdmin)

class FacturaAdmin(admin.ModelAdmin):
    list_display = ('Reserva', 'metodo', 'total', 'Estado')

admin.site.register(Factura, FacturaAdmin)