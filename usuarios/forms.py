# usuarios/forms.py
from django import forms
from .models import Usuario

class UsuarioForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Contraseña")

    class Meta:
        model = Usuario
        fields = ['username', 'email', 'password', 'rol']  # negocio NO se expone
        labels = {
            'username': 'Usuario',
            'email': 'Correo Electrónico',
            'rol': 'Rol',
        }
