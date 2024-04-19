from django.urls import path
from .views import home, Acercade, Cabañas, Restaurante, login_view, exit
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('logout/', exit, name='exit'),
    path('acercaDe/', Acercade, name='acercaDe'),
    path('cabañas/', Cabañas , name='cabañas'),
    path('restaurante/', Restaurante , name='restaurante'),
    path('login/', login_view , name='login'),
]
