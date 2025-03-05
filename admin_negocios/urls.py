from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

# Redirección de la raíz del sitio
def redirect_to_login(request):
    """Redirige a la página de login cuando se accede a la raíz del sitio."""
    return redirect('login')  # Usamos el nombre de la URL en lugar de la ruta directa

urlpatterns = [
    # Redirección para la página de inicio
    path('', redirect_to_login, name='root_redirect'),

    # Panel de administración de Django
    path('gestion/', admin.site.urls),

    # Módulo de usuarios
    path('usuarios/', include('usuarios.urls')),  # Incluye todas las URLs de usuarios

    # Módulo de inventario
    path('inventario/', include('inventario.urls')),  # Incluye todas las URLs de inventario

    # Módulo de finanzas
    path('finanzas/', include('finanzas.urls')),  # Incluye todas las URLs de finanzas
]