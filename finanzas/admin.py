from django.contrib import admin
from .models import IngresoEgreso

class IngresoEgresoAdmin(admin.ModelAdmin):
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser  # Solo superusuarios pueden eliminar

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser  # Solo superusuarios pueden modificar

admin.site.register(IngresoEgreso, IngresoEgresoAdmin)
