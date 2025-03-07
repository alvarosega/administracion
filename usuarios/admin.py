# usuarios/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario

class UsuarioAdmin(UserAdmin):
    list_display = ('username', 'email', 'rol', 'negocio', 'is_active')
    list_filter = ('rol', 'is_active', 'negocio')
    search_fields = ('username', 'email', 'negocio')
    ordering = ('username',)

    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Información Personal', {'fields': ('rol', 'negocio')}),
        ('Permisos', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'rol')}
        ),
    )

    def get_readonly_fields(self, request, obj=None):
        """
        Hace que 'negocio' y 'rol' sean solo lectura si se trata 
        de un admin ya creado y quien edita NO es superusuario.
        """
        if obj:
            if obj.rol == 'admin' and not request.user.is_superuser:
                return ['rol', 'negocio']
        return []

admin.site.register(Usuario, UsuarioAdmin)
