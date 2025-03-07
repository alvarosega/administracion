# usuarios/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Usuario
from .forms import UsuarioForm

def login_view(request):
    """
    Vista para iniciar sesión.
    Tras autenticar al usuario, redirige SIEMPRE a '/', que carga el index.html del proyecto principal.
    """
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')  # Carga index.html del proyecto principal
        else:
            messages.error(request, "Credenciales incorrectas. Intenta de nuevo.")

    return render(request, 'usuarios/login.html')


@login_required
def admin_dashboard(request):
    """
    Muestra el panel de administrador.
    Solo se accede si el usuario es rol='admin' y está autenticado.
    """
    if request.user.rol != 'admin':
        return redirect('/')  # Si no es admin, vuelve a index
    return render(request, 'usuarios/admin_dashboard.html')


@login_required
def empleado_dashboard(request):
    """
    Muestra el panel de empleado.
    Solo se accede si el usuario es rol='empleado' y está autenticado.
    """
    if request.user.rol != 'empleado':
        return redirect('/')  # Si no es empleado, vuelve a index
    return render(request, 'usuarios/empleado_dashboard.html')


@login_required
def lista_usuarios(request):
    """
    Lista de usuarios para que el admin gestione.
    - Muestra SOLO empleados del mismo negocio.
    - No muestra admins, para no poder modificarlos.
    """
    if request.user.rol != 'admin':
        return redirect('/')

    empleados = Usuario.objects.filter(negocio=request.user.negocio, rol='empleado')
    return render(request, 'usuarios/lista_usuarios.html', {'empleados': empleados})


@login_required
def crear_usuario(request):
    """
    Permite al admin crear empleados u otros admins, heredando su negocio.
    """
    if request.user.rol != 'admin':
        return redirect('/')

    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            nuevo = form.save(commit=False)
            # Asigna automáticamente el negocio del admin creador
            nuevo.negocio = request.user.negocio
            # Encripta la contraseña
            nuevo.set_password(form.cleaned_data['password'])
            nuevo.save()
            messages.success(request, "Usuario creado correctamente.")
            return redirect('lista_usuarios')
    else:
        form = UsuarioForm()

    return render(request, 'usuarios/form_usuario.html', {'form': form})


@login_required
def editar_usuario(request, usuario_id):
    """
    Editar un usuario (empleado) del mismo negocio.
    No permite editar admins.
    """
    if request.user.rol != 'admin':
        return redirect('/')

    usuario = get_object_or_404(Usuario, id=usuario_id, negocio=request.user.negocio)

    if usuario.rol == 'admin':
        messages.error(request, "No puedes editar a otro administrador.")
        return redirect('lista_usuarios')

    if request.method == 'POST':
        form = UsuarioForm(request.POST, instance=usuario)
        if form.is_valid():
            # Encripta la contraseña
            usuario.set_password(form.cleaned_data['password'])
            form.save()
            messages.success(request, "Empleado actualizado correctamente.")
            return redirect('lista_usuarios')
    else:
        form = UsuarioForm(instance=usuario)

    return render(request, 'usuarios/form_usuario.html', {'form': form})


@login_required
def eliminar_usuario(request, usuario_id):
    """
    Eliminar un usuario (empleado) del mismo negocio.
    No permite eliminar admins.
    """
    if request.user.rol != 'admin':
        return redirect('/')

    usuario = get_object_or_404(Usuario, id=usuario_id, negocio=request.user.negocio)
    if usuario.rol == 'admin':
        messages.error(request, "No puedes eliminar a otro administrador.")
        return redirect('lista_usuarios')

    usuario.delete()
    messages.success(request, "Empleado eliminado correctamente.")
    return redirect('lista_usuarios')
