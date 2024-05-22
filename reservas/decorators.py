from django.shortcuts import redirect
from django.urls import reverse

def login_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(reverse('login')) 
        return view_func(request, *args, **kwargs)

    return wrapper  