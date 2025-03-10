# finanzas/models.py

from django.db import models
from django.conf import settings
from django.utils import timezone

class MovimientoFinanciero(models.Model):
    """
    Representa un movimiento de dinero en el negocio:
    - INGRESO (por ventas, etc.)
    - EGRESO (por compras, gastos, etc.)
    """
    TIPO_CHOICES = [
        ('INGRESO', 'Ingreso'),
        ('EGRESO', 'Egreso'),
    ]

    negocio = models.CharField(max_length=150)
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateTimeField(default=timezone.now)
    descripcion = models.TextField(blank=True)
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.tipo} - {self.monto} ({self.negocio})"

    class Meta:
        ordering = ['-fecha']
