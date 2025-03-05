from django.urls import path
from .views import lista_productos, crear_producto, editar_producto, eliminar_producto, registrar_movimiento

urlpatterns = [
    path('productos/', lista_productos, name='lista_productos'),
    path('productos/crear/', crear_producto, name='crear_producto'),
    path('productos/editar/<int:producto_id>/', editar_producto, name='editar_producto'),
    path('productos/eliminar/<int:producto_id>/', eliminar_producto, name='eliminar_producto'),
    path('movimientos/registrar/', registrar_movimiento, name='registrar_movimiento'),
]