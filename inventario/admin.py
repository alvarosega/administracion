from django.contrib import admin
from .models import Negocio, Producto, MovimientoInventario, Proveedor

@admin.register(Negocio)
class NegocioAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')
    search_fields = ('nombre',)

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'tipo_producto', 'stock_actual', 'stock_minimo', 'precio_venta')
    list_filter = ('tipo_producto',)
    search_fields = ('nombre',)
    readonly_fields = ('fecha_actualizacion',)

@admin.register(MovimientoInventario)
class MovimientoInventarioAdmin(admin.ModelAdmin):
    list_display = ('id', 'producto', 'tipo', 'cantidad', 'fecha_movimiento', 'usuario')
    list_filter = ('tipo', 'fecha_movimiento')
    search_fields = ('producto__nombre', 'usuario__username')

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser  # Solo superusuarios pueden eliminar

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser  # Solo superusuarios pueden modificar

@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'telefono', 'correo')
    search_fields = ('nombre', 'correo')
