# admin_negocios/views.py
from django.shortcuts import render, redirect

def index(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'index.html')
