from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Producto, Estado, Cabaña, Reserva
from accounts.models import Profile


class RegisterForm(UserCreationForm):
    email = forms.EmailField(max_length=254)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['categoria', 'Estado', 'nomProducto', 'precio', 'descripcion', 'cantidad', 'imagen']
    

    def __init__(self, *args, **kwargs):
        super(ProductoForm, self).__init__(*args, **kwargs)
        # Filtrar las opciones del campo Estado
        self.fields['Estado'].queryset = Estado.objects.filter(id__in=[ 1])

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image', 'address', 'telephone']

class UserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

class CabañaForm(forms.ModelForm):
    class Meta:
        model = Cabaña
        fields = ['nomCabaña', 'perMax', 'precio', 'descripcion', 'imagen']