# inventario/admin.py
from django.contrib import admin
from .models import Producto, MovimientoInventario  # Quitar Negocio

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    pass

@admin.register(MovimientoInventario)
class MovimientoInventarioAdmin(admin.ModelAdmin):
    pass

