# inventario/urls.py
from django.urls import path
from .views import (
    lista_productos,
    crear_producto,
    editar_producto,
    eliminar_producto,
    lista_lotes,
    crear_lote,
    editar_lote,
    eliminar_lote,
    registrar_venta,
    movimientos_inventario,
    importar_inventario,
    descargar_plantilla_inventario,
)

urlpatterns = [
    # PRODUCTOS
    path('productos/', lista_productos, name='lista_productos'),
    path('productos/crear/', crear_producto, name='crear_producto'),
    path('productos/editar/<int:producto_id>/', editar_producto, name='editar_producto'),
    path('productos/eliminar/<int:producto_id>/', eliminar_producto, name='eliminar_producto'),

    # LOTES
    path('lotes/<int:producto_id>/', lista_lotes, name='lista_lotes'),
    path('lotes/<int:producto_id>/crear/', crear_lote, name='crear_lote'),
    path('lotes/editar/<int:lote_id>/', editar_lote, name='editar_lote'),
    path('lotes/eliminar/<int:lote_id>/', eliminar_lote, name='eliminar_lote'),

    # MOVIMIENTOS
    path('venta/<int:lote_id>/', registrar_venta, name='registrar_venta'),
    path('movimientos/', movimientos_inventario, name='movimientos_inventario'),

    # IMPORTAR INVENTARIO
    path('importar/', importar_inventario, name='importar_inventario'),
    
    path('descargar_plantilla/', descargar_plantilla_inventario, name='descargar_plantilla_inventario'),

]
