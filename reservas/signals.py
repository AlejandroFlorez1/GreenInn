from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Reserva, Pedido

@receiver(post_save, sender=Reserva)
def crear_pedido(sender, instance, created, **kwargs):
    if created:
        Pedido.objects.create(Reserva=instance, estado=instance.estado)