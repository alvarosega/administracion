from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import MovimientoInventario, Producto
from .forms import MovimientoInventarioForm

@login_required
def lista_productos(request):
    """Muestra la lista de productos del negocio del usuario."""
    productos = Producto.objects.filter(negocio=request.user.negocio)
    return render(request, 'inventario/lista_productos.html', {'productos': productos})

@login_required
def crear_producto(request):
    """Permite al administrador crear un nuevo producto."""
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            producto = form.save(commit=False)
            producto.negocio = request.user.negocio  # Asignar el negocio del usuario
            producto.save()
            messages.success(request, "Producto creado correctamente.")
            return redirect('lista_productos')
    else:
        form = ProductoForm()

    return render(request, 'inventario/form_producto.html', {'form': form})

@login_required
def editar_producto(request, producto_id):
    """Permite editar un producto existente."""
    producto = get_object_or_404(Producto, id=producto_id, negocio=request.user.negocio)
    
    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            messages.success(request, "Producto actualizado correctamente.")
            return redirect('lista_productos')
    else:
        form = ProductoForm(instance=producto)

    return render(request, 'inventario/form_producto.html', {'form': form})

@login_required
def eliminar_producto(request, producto_id):
    """Permite eliminar un producto."""
    producto = get_object_or_404(Producto, id=producto_id, negocio=request.user.negocio)
    producto.delete()
    messages.success(request, "Producto eliminado correctamente.")
    return redirect('lista_productos')

@login_required
def registrar_movimiento(request):
    """Permite registrar un movimiento de inventario (entrada o salida)."""
    if request.method == 'POST':
        form = MovimientoInventarioForm(request.POST)
        if form.is_valid():
            movimiento = form.save(commit=False)
            movimiento.negocio = request.user.negocio  # Asignar el negocio del usuario
            movimiento.usuario = request.user  # Asignar el usuario actual
            movimiento.save()
            messages.success(request, "Movimiento registrado correctamente.")
            return redirect('lista_productos')
    else:
        form = MovimientoInventarioForm()

    return render(request, 'inventario/registrar_movimiento.html', {'form': form})