from django import forms
from .models import IngresoEgreso

class IngresoEgresoForm(forms.ModelForm):
    class Meta:
        model = IngresoEgreso
        fields = ['tipo', 'monto', 'descripcion']