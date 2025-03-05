from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import IngresoEgreso
from .forms import IngresoEgresoForm
from django.http import HttpResponse
import csv

@login_required
def lista_finanzas(request):
    """Muestra la lista de registros financieros del negocio del usuario."""
    finanzas = IngresoEgreso.objects.filter(negocio=request.user.negocio)
    return render(request, 'finanzas/lista_finanzas.html', {'finanzas': finanzas})

@login_required
def crear_finanza(request):
    """Permite al administrador crear un nuevo registro financiero."""
    if request.method == 'POST':
        form = IngresoEgresoForm(request.POST)
        if form.is_valid():
            finanza = form.save(commit=False)
            finanza.negocio = request.user.negocio  # Asignar el negocio del usuario
            finanza.usuario = request.user  # Asignar el usuario actual
            finanza.save()
            messages.success(request, "Registro financiero creado correctamente.")
            return redirect('lista_finanzas')
    else:
        form = IngresoEgresoForm()

    return render(request, 'finanzas/form_finanza.html', {'form': form})

@login_required
def editar_finanza(request, finanza_id):
    """Permite editar un registro financiero existente."""
    finanza = get_object_or_404(IngresoEgreso, id=finanza_id, negocio=request.user.negocio)
    
    if request.method == 'POST':
        form = IngresoEgresoForm(request.POST, instance=finanza)
        if form.is_valid():
            form.save()
            messages.success(request, "Registro financiero actualizado correctamente.")
            return redirect('lista_finanzas')
    else:
        form = IngresoEgresoForm(instance=finanza)

    return render(request, 'finanzas/form_finanza.html', {'form': form})

@login_required
def eliminar_finanza(request, finanza_id):
    """Permite eliminar un registro financiero."""
    finanza = get_object_or_404(IngresoEgreso, id=finanza_id, negocio=request.user.negocio)
    finanza.delete()
    messages.success(request, "Registro financiero eliminado correctamente.")
    return redirect('lista_finanzas')

@login_required
def exportar_reportes(request):
    """Exporta los registros financieros a un archivo CSV."""
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="reporte_finanzas.csv"'

    writer = csv.writer(response)
    writer.writerow(['Tipo', 'Monto', 'Descripción', 'Fecha'])

    finanzas = IngresoEgreso.objects.filter(negocio=request.user.negocio)
    for finanza in finanzas:
        writer.writerow([finanza.tipo, finanza.monto, finanza.descripcion, finanza.fecha_movimiento])

    return response