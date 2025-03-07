from django.contrib import admin
from django.urls import path, include
from .views import index  # Importamos la nueva vista index

urlpatterns = [
    path('', index, name='index'),  # Asegura que el index está en la raíz

    # Panel de administración de Django
    path('gestion/', admin.site.urls),

    # Módulo de usuarios
    path('usuarios/', include('usuarios.urls')),

    # Módulo de inventario
    path('inventario/', include('inventario.urls')),

    # Módulo de finanzas
    path('finanzas/', include('finanzas.urls')),
]
