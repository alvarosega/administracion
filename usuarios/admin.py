from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario

class UsuarioAdmin(UserAdmin):
    list_display = ('username', 'email', 'rol', 'negocio', 'is_active')  # Mostrar en la lista
    list_filter = ('rol', 'is_active', 'negocio')  # Agregar filtros en el panel de admin
    search_fields = ('username', 'email', 'negocio__nombre')  # Búsqueda en admin
    ordering = ('username',)

    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Información Personal', {'fields': ('rol', 'negocio')}),
        ('Permisos', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'rol', 'negocio')}
        ),
    )

admin.site.register(Usuario, UsuarioAdmin)
