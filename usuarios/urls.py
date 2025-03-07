# usuarios/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (
    login_view,
    admin_dashboard,
    empleado_dashboard,
    lista_usuarios,
    crear_usuario,
    editar_usuario,
    eliminar_usuario,
)

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('admin/', admin_dashboard, name='admin_dashboard'),
    path('empleado/', empleado_dashboard, name='empleado_dashboard'),

    path('usuarios/', lista_usuarios, name='lista_usuarios'),
    path('usuarios/crear/', crear_usuario, name='crear_usuario'),
    path('usuarios/editar/<int:usuario_id>/', editar_usuario, name='editar_usuario'),
    path('usuarios/eliminar/<int:usuario_id>/', eliminar_usuario, name='eliminar_usuario'),
]
