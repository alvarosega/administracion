from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Usuario
from .forms import UsuarioForm

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

@login_required
def empleado_dashboard(request):
    """Vista del panel de empleados."""
    if request.user.rol != 'empleado':
        return redirect('index')  # Redirigir si no es empleado
    return render(request, 'usuarios/empleado_dashboard.html')

@login_required
def admin_dashboard(request):
    """Vista del panel de administradores."""
    if request.user.rol != 'admin':
        return redirect('index')  # Redirigir si no es administrador
    return render(request, 'usuarios/admin_dashboard.html')

@login_required
def lista_usuarios(request):
    """Lista los empleados del negocio del administrador."""
    if request.user.rol != 'admin':
        return redirect('index')  # Redirigir si no es administrador
    
    empleados = Usuario.objects.filter(negocio=request.user.negocio, rol='empleado')
    return render(request, 'usuarios/lista_usuarios.html', {'empleados': empleados})

@login_required
def crear_usuario(request):
    """Permite al administrador agregar un empleado a su negocio."""
    if request.user.rol != 'admin':
        return redirect('index')  

    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            usuario = form.save(commit=False)
            usuario.negocio = request.user.negocio  # Asigna el negocio del admin
            usuario.rol = 'empleado'  # Solo puede crear empleados
            usuario.set_password(form.cleaned_data['password'])  # Encripta contraseña
            usuario.save()
            messages.success(request, "Empleado agregado correctamente.")
            return redirect('lista_usuarios')
    else:
        form = UsuarioForm()

    return render(request, 'usuarios/form_usuario.html', {'form': form})

@login_required
def editar_usuario(request, usuario_id):
    """Permite editar un usuario del negocio."""
    usuario = get_object_or_404(Usuario, id=usuario_id, negocio=request.user.negocio, rol='empleado')
    
    if request.method == 'POST':
        form = UsuarioForm(request.POST, instance=usuario)
        if form.is_valid():
            usuario.set_password(form.cleaned_data['password'])  # Encripta contraseña si es nueva
            form.save()
            messages.success(request, "Empleado actualizado correctamente.")
            return redirect('lista_usuarios')
    else:
        form = UsuarioForm(instance=usuario)

    return render(request, 'usuarios/form_usuario.html', {'form': form})

@login_required
def eliminar_usuario(request, usuario_id):
    """Permite al administrador eliminar empleados dentro de su negocio."""
    usuario = get_object_or_404(Usuario, id=usuario_id, negocio=request.user.negocio, rol='empleado')
    usuario.delete()
    messages.success(request, "Empleado eliminado correctamente.")
    return redirect('lista_usuarios')

def index(request):
    """Vista principal que muestra el panel según el rol del usuario."""
    es_admin = request.user.rol == 'admin'
    return render(request, 'index.html', {'es_admin': es_admin})