from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, authenticate, login
# Create your views here.


def login_view(request):
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            User = authenticate(request, username=username, password=password)
            if User is not None:
                login(request, User)
                return redirect('home')
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
