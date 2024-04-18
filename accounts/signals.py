from django.contrib.auth.models import Group
from .models import Profile
from django.dispatch import receiver
from django.db.models.signals import post_save

@receiver(post_save, sender=Profile)
def add_users_to_Usuarios_group(sender, instance, created, **kwargs):
    if created:
        try:
            group1 = Group.objects.get(name='usuario')
        except Group.DoesNotExist:
            group1 = Group.objects.create(name='usuario')
            group2 = Group.objects.create(name='administrativo')
            Group3  = Group.objects.create(name='adminSystem')
        instance.user.groups.add(group1)



