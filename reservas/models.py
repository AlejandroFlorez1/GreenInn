from django.db import models
from django.contrib.auth.models import User
# Create your models here.

#categoria Producto
class Categoria(models.Model):
    nomCategoria  = models.CharField(max_length=30, verbose_name='Nombre de la categoria')

    def __str__(self):
        return self.nomCategoria
    
    class Meta:
        verbose_name = 'categoria'
        verbose_name_plural = 'categorias'
    
#Estado
class Estado(models.Model):
    tipEstado = models.CharField(max_length=15, verbose_name='Tipo de estado')

    def __str__(self):
        return self.tipEstado
    
    class Meta:
        verbose_name = 'estado'
        verbose_name_plural = 'estados'

#Cabaña
class Cabaña(models.Model):
    nomCabaña = models.CharField(max_length=20, verbose_name='Cabaña')
    perMax = models.PositiveIntegerField(default=1, verbose_name='Personas maximas')
    precio = models.FloatField(default=0, verbose_name='Precio')
    descripcion = models.CharField(max_length=70, null=True, blank=True, verbose_name='Descripción')
    imagen = models.ImageField(upload_to='images_Cabañas', null=True, blank=True, verbose_name='Imagen')

    def __str__(self):
        return self.nomCabaña
    
    class Meta:
        verbose_name = 'Cabaña'
        verbose_name_plural = 'Cabañas'

#Reserva
class Reserva(models.Model):
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE, verbose_name='Estado')
    cabana = models.ForeignKey(Cabaña, on_delete=models.CASCADE, verbose_name='Cabaña')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='usuario_reserva', verbose_name='Usuario')
    fechaReserva = models.DateField(auto_now_add=True,verbose_name='Fecha de reserva')
    fechaCheckIn = models.DateField(verbose_name='Fecha de check in')
    fechaCheckOut = models.DateField(verbose_name='Fecha de check out')
    numPersonas = models.PositiveIntegerField(default=7, verbose_name='Personas')

    def __str__(self):
        return f"{self.cabana} - {self.usuario}"
    class Meta:
        verbose_name = 'reserva'
        verbose_name_plural = 'reservas'

#Pedido
class Pedido(models.Model):
    Reserva = models.ForeignKey(Reserva, on_delete=models.CASCADE, related_name='Reserva_pedido', verbose_name='Reserva')
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE, verbose_name='Estado')
    fechaHora = models.DateTimeField(auto_now_add=True, verbose_name='Fecha y hora')

    def __str__(self):
        return f"{self.Reserva} - {self.estado}"
    
    class Meta:
        verbose_name = 'pedido'
        verbose_name_plural = 'pedidos'


#Producto
class Producto(models.Model):
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, verbose_name='Categoriá')
    Estado = models.ForeignKey(Estado, on_delete=models.CASCADE, verbose_name='Estado')
    nomProducto = models.CharField(max_length=30, verbose_name='Nombre del producto')
    precio = models.FloatField(default=0, verbose_name='Precio')
    descripcion = models.CharField(max_length=50, null=True, blank=True, verbose_name='Descripción')
    cantidad = models.PositiveIntegerField(default=1, verbose_name='Cantidad')
    imagen = models.ImageField(upload_to='images_productos', null=True, blank=True, verbose_name='Imagen')

    def __str__(self):
        return self.nomProducto
    
    class Meta:
        verbose_name = 'producto'
        verbose_name_plural = 'productos'

#Pedido_Producto
class Pedido_Producto(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, verbose_name='Pedido')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, verbose_name='producto')

    def __str__(self):
        return f"{self.pedido} - {self.producto}"
    
    class Meta:
        verbose_name = 'pedido_producto'
        verbose_name_plural = 'pedidos_productos'

#Metodo de pago
class Metodo_Pago(models.Model):
    nomMetodo = models.CharField(max_length=30, verbose_name='Metodo de pago')

    def __str__(self):
        return self.nomMetodo
    
    class Meta:
        verbose_name = 'metodo de pago'
        verbose_name_plural = 'metodos de pago'

#Factura
class Factura(models.Model):
    Reserva = models.ForeignKey(Reserva, on_delete=models.CASCADE, related_name='Reserva_factura', verbose_name='Reserva')
    metodo = models.ForeignKey(Metodo_Pago, on_delete=models.CASCADE, verbose_name='Metodo de pago')
    Estado = models.ForeignKey(Estado, on_delete=models.CASCADE, verbose_name='Estado')
    total = models.FloatField(default=0, verbose_name='Total')


    def __str__(self):
        return f"{self.pedido} - {self.metodo}"
    
    class Meta:
        verbose_name = 'factura'
        verbose_name_plural = 'facturas'


