from django.urls import path
from .views import home, Acercade, Cabañas, Restaurante, login_view, exit, inicio, User_Reservas, User_Historial_Reservas, User_Hacer_Reserva, User_Profile
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('salir/', exit, name='exit'),
    path('acercaDe/', Acercade, name='acercaDe'),
    path('cabañas/', Cabañas , name='cabañas'),
    path('restaurante/', Restaurante , name='restaurante'),
    path('login/', login_view , name='login'),
    path('Inicio/', inicio , name='inicio'),
    path('User_Reservas/', User_Reservas , name='User_Reservas'),
    path('User_Historial_Reservas/', User_Historial_Reservas , name='User_Historial_Reservas'),
    path('User_Hacer_Reserva/', User_Hacer_Reserva , name='User_Hacer_Reserva'),
    path('Profile/', User_Profile, name='user_profile'),
]


