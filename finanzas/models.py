from django.db import models

# Importar el modelo de negocio correctamente
from inventario.models import Negocio, MovimientoInventario
from usuarios.models import Usuario

class IngresoEgreso(models.Model):
    negocio = models.ForeignKey(Negocio, on_delete=models.CASCADE)
    tipo = models.CharField(choices=[('ingreso', 'Ingreso'), ('egreso', 'Egreso')], max_length=10)
    monto = models.DecimalField(max_digits=12, decimal_places=2)
    descripcion = models.TextField(blank=True, null=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True)
    fecha_movimiento = models.DateTimeField(auto_now_add=True)
    movimiento_inventario = models.ForeignKey(MovimientoInventario, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.tipo} - {self.monto}"
