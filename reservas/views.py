from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
# Create your views here.

def helloword(request):
    return render(request, 'Login/Login.html', {'form': UserCreationForm})

@login_required
def Productos(request):
    return render(request, 'Core/main.html', {'form': UserCreationForm})

def home(request):
    return render(request, 'Core/home.html', {'form': UserCreationForm})

def exit(request):
    logout(request)
    return redirect('home')
