# inventario/forms.py
from django import forms
from .models import Producto, Lote, MovimientoInventario

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = [
            'negocio',
            'nombre',
            'tipo_producto',
            'descripcion',
            'precio_compra',
            'precio_venta',
            'stock_minimo',
            'permitir_stock_negativo',
        ]


class LoteForm(forms.ModelForm):
    class Meta:
        model = Lote
        fields = ['producto', 'cantidad', 'fecha_vencimiento']


class RegistrarVentaForm(forms.Form):
    """
    Formulario para que el empleado registre una venta (salida).
    Selecciona el lote, la cantidad y un comentario opcional.
    """
    lote_id = forms.IntegerField(widget=forms.HiddenInput())  # Se pasa por la URL o un select
    cantidad = forms.IntegerField(min_value=1)
    comentario = forms.CharField(widget=forms.Textarea, required=False)


class ImportarInventarioForm(forms.Form):
    """
    Form para subir un archivo CSV/Excel con datos de productos y/o lotes.
    """
    archivo = forms.FileField()
    # Podrías añadir más campos según la lógica de importación
