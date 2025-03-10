# finanzas/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
import csv
from .models import MovimientoFinanciero
from .forms import EgresoForm
from django.utils import timezone
from datetime import datetime

@login_required
def registrar_egreso(request):
    """
    Vista para que el admin registre manualmente un egreso (no relacionado a la compra de lotes).
    """
    if request.user.rol != 'admin':
        return redirect('/')  # Empleado no ve finanzas

    if request.method == 'POST':
        form = EgresoForm(request.POST)
        if form.is_valid():
            egreso = form.save(commit=False)
            egreso.tipo = 'EGRESO'
            egreso.negocio = request.user.negocio
            egreso.usuario = request.user
            egreso.save()
            messages.success(request, "Egreso registrado correctamente.")
            return redirect('resumen_financiero')
    else:
        form = EgresoForm()

    return render(request, 'finanzas/registrar_egreso.html', {'form': form})


@login_required
def resumen_financiero(request):
    """
    Muestra un resumen de ingresos y egresos para el negocio del usuario admin.
    También un balance general y estado de resultados.
    """
    if request.user.rol != 'admin':
        return redirect('/')

    # Filtrar por negocio
    movimientos = MovimientoFinanciero.objects.filter(negocio=request.user.negocio)

    # Filtrar por rango de fechas (opcional)
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')

    if fecha_inicio and fecha_fin:
        try:
            inicio_dt = datetime.strptime(fecha_inicio, '%Y-%m-%d')
            fin_dt = datetime.strptime(fecha_fin, '%Y-%m-%d')
            # Ajustar fin_dt para incluir todo el día
            fin_dt = fin_dt.replace(hour=23, minute=59, second=59)
            movimientos = movimientos.filter(fecha__range=(inicio_dt, fin_dt))
        except ValueError:
            messages.error(request, "Formato de fecha inválido (use YYYY-MM-DD).")

    # Calcular totales
    total_ingresos = sum(m.monto for m in movimientos if m.tipo == 'INGRESO')
    total_egresos = sum(m.monto for m in movimientos if m.tipo == 'EGRESO')
    utilidad = total_ingresos - total_egresos

    context = {
        'movimientos': movimientos,
        'total_ingresos': total_ingresos,
        'total_egresos': total_egresos,
        'utilidad': utilidad,
        'fecha_inicio': fecha_inicio,
        'fecha_fin': fecha_fin,
    }
    return render(request, 'finanzas/resumen_financiero.html', context)


@login_required
def exportar_finanzas_csv(request):
    """
    Exporta los movimientos financieros del negocio a un archivo CSV.
    """
    if request.user.rol != 'admin':
        return redirect('/')

    movimientos = MovimientoFinanciero.objects.filter(negocio=request.user.negocio).order_by('-fecha')

    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename="finanzas.csv"'},
    )

    writer = csv.writer(response, delimiter=';', quotechar='"')
    writer.writerow(['tipo', 'monto', 'fecha', 'descripcion', 'usuario'])

    for mov in movimientos:
        usuario_str = mov.usuario.username if mov.usuario else ''
        writer.writerow([
            mov.tipo,
            mov.monto,
            mov.fecha.strftime('%Y-%m-%d %H:%M:%S'),
            mov.descripcion,
            usuario_str
        ])

    return response
