# finanzas/forms.py
from django import forms
from .models import MovimientoFinanciero

class EgresoForm(forms.ModelForm):
    """
    Formulario para registrar egresos manuales.
    """
    class Meta:
        model = MovimientoFinanciero
        fields = ['monto', 'fecha', 'descripcion']
        # 'negocio' y 'tipo' se asignan automáticamente en la vista
