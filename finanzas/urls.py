# finanzas/urls.py
from django.urls import path
from .views import (
    registrar_egreso,
    resumen_financiero,
    exportar_finanzas_csv
)

urlpatterns = [
    path('egreso/', registrar_egreso, name='registrar_egreso'),
    path('resumen/', resumen_financiero, name='resumen_financiero'),
    path('exportar_csv/', exportar_finanzas_csv, name='exportar_finanzas_csv'),
]
