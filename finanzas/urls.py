from django.urls import path
from .views import lista_finanzas, crear_finanza, editar_finanza, eliminar_finanza, exportar_reportes

urlpatterns = [
    path('finanzas/', lista_finanzas, name='lista_finanzas'),
    path('finanzas/crear/', crear_finanza, name='crear_finanza'),
    path('finanzas/editar/<int:finanza_id>/', editar_finanza, name='editar_finanza'),
    path('finanzas/eliminar/<int:finanza_id>/', eliminar_finanza, name='eliminar_finanza'),
    path('finanzas/exportar/', exportar_reportes, name='exportar_reportes'),
]