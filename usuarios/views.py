from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

def login_view(request):
    """Vista para iniciar sesión y redirigir a la página principal."""
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')  # Redirigir a la página principal
        else:
            messages.error(request, "Credenciales incorrectas. Intenta de nuevo.")

    return render(request, 'usuarios/login.html')