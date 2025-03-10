from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.utils import timezone

import csv
import io

from .models import Producto, Lote, MovimientoInventario
from .forms import (
    ProductoForm,
    LoteForm,
    RegistrarVentaForm,
    ImportarInventarioForm
)

# Importamos el modelo financiero para crear ingresos/egresos automáticos
from finanzas.models import MovimientoFinanciero

# --- VISTAS DE PRODUCTO ---

@login_required
def lista_productos(request):
    """
    Muestra todos los productos filtrados por el negocio del usuario.
    Empleados pueden ver, admins pueden crear/editar/eliminar.
    """
    productos = Producto.objects.filter(negocio=request.user.negocio)
    return render(request, 'inventario/lista_productos.html', {'productos': productos})


@login_required
def crear_producto(request):
    """
    Solo admin crea productos. Empleado no puede.
    """
    if request.user.rol != 'admin':
        return redirect('lista_productos')

    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            nuevo = form.save(commit=False)
            # Si quisieras forzar el negocio del usuario:
            # nuevo.negocio = request.user.negocio
            nuevo.save()
            messages.success(request, "Producto creado correctamente.")
            return redirect('lista_productos')
    else:
        form = ProductoForm()

    return render(request, 'inventario/form_producto.html', {'form': form})


@login_required
def editar_producto(request, producto_id):
    if request.user.rol != 'admin':
        return redirect('lista_productos')

    producto = get_object_or_404(
        Producto, id=producto_id, negocio=request.user.negocio
    )

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
    if request.user.rol != 'admin':
        return redirect('lista_productos')

    producto = get_object_or_404(
        Producto, id=producto_id, negocio=request.user.negocio
    )
    producto.delete()
    messages.success(request, "Producto eliminado.")
    return redirect('lista_productos')


# --- VISTAS DE LOTE ---

@login_required
def lista_lotes(request, producto_id):
    """
    Muestra los lotes de un producto en particular.
    """
    producto = get_object_or_404(
        Producto, id=producto_id, negocio=request.user.negocio
    )
    lotes = Lote.objects.filter(producto=producto)
    return render(request, 'inventario/lista_lotes.html', {
        'producto': producto,
        'lotes': lotes
    })


@login_required
def crear_lote(request, producto_id):
    """
    Solo el admin crea lotes. El empleado no puede.
    Además, se registra un EGRESO automático en finanzas.
    """
    if request.user.rol != 'admin':
        return redirect('lista_productos')

    producto = get_object_or_404(
        Producto, id=producto_id, negocio=request.user.negocio
    )

    if request.method == 'POST':
        form = LoteForm(request.POST)
        if form.is_valid():
            lote = form.save(commit=False)
            lote.producto = producto
            lote.save()

            # Registrar Egreso automático por compra de stock
            costo_compra = lote.cantidad * producto.precio_compra
            MovimientoFinanciero.objects.create(
                negocio=request.user.negocio,
                tipo='EGRESO',
                monto=costo_compra,
                fecha=timezone.now(),
                descripcion=f"Compra de {lote.cantidad} uds de {producto.nombre}",
                usuario=request.user
            )

            messages.success(request, "Lote creado y egreso registrado.")
            return redirect('lista_lotes', producto_id=producto.id)
    else:
        form = LoteForm()

    return render(request, 'inventario/form_lote.html', {
        'form': form,
        'producto': producto
    })


@login_required
def editar_lote(request, lote_id):
    """
    Editar un lote existente (solo admin).
    """
    if request.user.rol != 'admin':
        return redirect('lista_productos')

    lote = get_object_or_404(Lote, id=lote_id)
    # Verificamos que el lote pertenezca al negocio del user
    if lote.producto.negocio != request.user.negocio:
        return redirect('lista_productos')

    if request.method == 'POST':
        form = LoteForm(request.POST, instance=lote)
        if form.is_valid():
            form.save()
            messages.success(request, "Lote actualizado correctamente.")
            return redirect('lista_lotes', producto_id=lote.producto.id)
    else:
        form = LoteForm(instance=lote)

    return render(request, 'inventario/form_lote.html', {
        'form': form,
        'producto': lote.producto
    })


@login_required
def eliminar_lote(request, lote_id):
    """
    Eliminar un lote (solo admin).
    """
    if request.user.rol != 'admin':
        return redirect('lista_productos')

    lote = get_object_or_404(Lote, id=lote_id)
    if lote.producto.negocio != request.user.negocio:
        return redirect('lista_productos')

    producto_id = lote.producto.id
    lote.delete()
    messages.success(request, "Lote eliminado.")
    return redirect('lista_lotes', producto_id=producto_id)


# --- REGISTRAR VENTAS (EMPLEADO/ADMIN) ---

@login_required
def registrar_venta(request, lote_id):
    """
    El empleado (o admin) registra una venta (salida).
    - No se puede vender más stock del que hay en el lote.
    - Registra un INGRESO automático en finanzas.
    """
    lote = get_object_or_404(Lote, id=lote_id)

    # Validar que sea el mismo negocio
    if lote.producto.negocio != request.user.negocio:
        return redirect('lista_productos')

    # Validar rol (admin o empleado)
    if request.user.rol not in ['admin', 'empleado']:
        return redirect('lista_productos')

    if request.method == 'POST':
        form = RegistrarVentaForm(request.POST)
        if form.is_valid():
            cantidad_vendida = form.cleaned_data['cantidad']
            comentario = form.cleaned_data['comentario']

            # VALIDACIÓN: No se puede vender más de lo que hay en el lote
            if cantidad_vendida > lote.cantidad:
                messages.error(request, f"La venta excede el stock disponible ({lote.cantidad} unidades).")
                return redirect('registrar_venta', lote_id=lote.id)

            # Crear movimiento de inventario
            movimiento = MovimientoInventario.objects.create(
                negocio=request.user.negocio,
                producto=lote.producto,
                lote=lote,
                tipo_movimiento='VENTA',
                cantidad=cantidad_vendida,
                usuario=request.user,
                comentario=comentario
            )

            # Calcular el monto de la venta
            monto_venta = cantidad_vendida * lote.producto.precio_venta

            # Registrar INGRESO automático en finanzas
            MovimientoFinanciero.objects.create(
                negocio=request.user.negocio,
                tipo='INGRESO',
                monto=monto_venta,
                fecha=timezone.now(),
                descripcion=f"Venta de {cantidad_vendida} uds de {lote.producto.nombre}",
                usuario=request.user
            )

            messages.success(request, "Venta registrada correctamente (finanzas actualizadas).")
            return redirect('lista_lotes', producto_id=lote.producto.id)
    else:
        form = RegistrarVentaForm(initial={'lote_id': lote.id})

    return render(request, 'inventario/registrar_venta.html', {
        'form': form,
        'lote': lote
    })


# --- HISTORIAL DE MOVIMIENTOS DE INVENTARIO ---

@login_required
def movimientos_inventario(request):
    """
    Lista todos los movimientos del negocio actual, ordenados por fecha descendente.
    """
    movs = MovimientoInventario.objects.filter(
        negocio=request.user.negocio
    ).order_by('-fecha_movimiento')

    return render(request, 'inventario/movimientos_inventario.html', {'movimientos': movs})


# --- IMPORTAR INVENTARIO (CSV) ---

@login_required
def importar_inventario(request):
    """
    Permite al admin subir un archivo CSV con la estructura:
    [nombre, tipo_producto, descripcion, precio_compra, precio_venta, stock_minimo, cantidad, fecha_vencimiento]
    para crear/actualizar productos y crear lotes.
    """
    if request.user.rol != 'admin':
        return redirect('lista_productos')

    if request.method == 'POST':
        form = ImportarInventarioForm(request.POST, request.FILES)
        if form.is_valid():
            archivo = request.FILES['archivo']
            data_set = archivo.read().decode('UTF-8')
            io_string = io.StringIO(data_set)
            # Usar el mismo delimitador que se usó al descargar la plantilla
            csv_reader = csv.reader(io_string, delimiter=';')

            def to_float(value):
                if value == '' or value.lower() == 'null':
                    return 0.0
                return float(value)

            encabezado = True
            for fila in csv_reader:
                # Saltar la fila de encabezado
                if encabezado:
                    encabezado = False
                    continue

                try:
                    # [nombre, tipo_producto, descripcion, precio_compra, precio_venta, stock_minimo, cantidad, fecha_vencimiento]
                    nombre = fila[0]
                    tipo_producto = fila[1]
                    descripcion = fila[2]
                    precio_compra = to_float(fila[3])
                    precio_venta = to_float(fila[4])
                    stock_minimo = int(fila[5]) if fila[5] not in ('', 'null') else 0
                    cantidad = int(fila[6]) if fila[6] not in ('', 'null') else 0
                    fecha_venc = fila[7].strip().lower() if len(fila) > 7 else ''

                    # Crear o actualizar Producto
                    producto, creado = Producto.objects.get_or_create(
                        negocio=request.user.negocio,
                        nombre=nombre,
                        defaults={
                            'tipo_producto': tipo_producto,
                            'descripcion': descripcion,
                            'precio_compra': precio_compra,
                            'precio_venta': precio_venta,
                            'stock_minimo': stock_minimo
                        }
                    )
                    if not creado:
                        # Actualizar campos si el producto ya existía
                        producto.tipo_producto = tipo_producto
                        producto.descripcion = descripcion
                        producto.precio_compra = precio_compra
                        producto.precio_venta = precio_venta
                        producto.stock_minimo = stock_minimo
                        producto.save()

                    # Crear un lote con la cantidad
                    lote = Lote.objects.create(
                        producto=producto,
                        cantidad=cantidad
                    )

                    # Asignar fecha de vencimiento si aplica
                    if fecha_venc and fecha_venc != 'null':
                        # Asumiendo que viene en formato YYYY-MM-DD
                        lote.fecha_vencimiento = fecha_venc
                        lote.save()

                except Exception as e:
                    messages.error(request, f"Error procesando fila: {fila}. Detalle: {e}")
                    continue

            messages.success(request, "Archivo importado correctamente.")
            return redirect('lista_productos')
    else:
        form = ImportarInventarioForm()

    return render(request, 'inventario/importar_inventario.html', {'form': form})


@login_required
def descargar_plantilla_inventario(request):
    """
    Descarga una plantilla CSV con las columnas necesarias
    para importar el inventario.
    """
    if request.user.rol != 'admin':
        return redirect('lista_productos')

    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename="plantilla_inventario.csv"'},
    )

    writer = csv.writer(response, delimiter=';', quotechar='"')
    writer.writerow([
        'nombre',
        'tipo_producto',
        'descripcion',
        'precio_compra',
        'precio_venta',
        'stock_minimo',
        'cantidad',
        'fecha_vencimiento'
    ])

    return response
