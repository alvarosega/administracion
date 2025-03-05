from django.urls import path
from .views import (
    login_view, 
    empleado_dashboard, 
    admin_dashboard, 
    lista_usuarios, 
    crear_usuario, 
    editar_usuario, 
    eliminar_usuario, 
    index  # Asegúrate de que esta vista esté definida en views.py
)

urlpatterns = [
    path('', index, name='index'),  # Página principal (index)
    path('login/', login_view, name='login'),  # URL para el login
    path('empleado/', empleado_dashboard, name='empleado_dashboard'),  # Panel de empleado
    path('admin/', admin_dashboard, name='admin_dashboard'),  # Panel de administrador
    path('usuarios/', lista_usuarios, name='lista_usuarios'),  # Lista de usuarios
    path('usuarios/crear/', crear_usuario, name='crear_usuario'),  # Crear usuario
    path('usuarios/editar/<int:usuario_id>/', editar_usuario, name='editar_usuario'),  # Editar usuario
    path('usuarios/eliminar/<int:usuario_id>/', eliminar_usuario, name='eliminar_usuario'),  # Eliminar usuario
]