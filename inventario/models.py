# inventario/models.py

from django.db import models
from django.conf import settings  # Para referenciar al modelo Usuario
from django.utils import timezone

class Producto(models.Model):
    negocio = models.CharField(max_length=150, null=False, blank=False)
    nombre = models.CharField(max_length=150)
    tipo_producto = models.CharField(max_length=100, blank=True)
    descripcion = models.TextField(blank=True)
    precio_compra = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    precio_venta = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    stock_minimo = models.PositiveIntegerField(default=0)  # Para alertas
    permitir_stock_negativo = models.BooleanField(default=False)  # Admin decide

    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nombre} ({self.negocio})"

    @property
    def stock_total(self):
        """
        Suma la cantidad de todos los lotes activos para obtener el stock total del producto.
        """
        lotes = self.lote_set.all()  # Relación inversa
        return sum(l.cantidad for l in lotes)

    def alerta_stock_minimo(self):
        """
        Retorna True si el stock total es menor que stock_minimo.
        """
        return self.stock_total < self.stock_minimo


class Lote(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=0)
    fecha_vencimiento = models.DateField(null=True, blank=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Lote de {self.producto.nombre} - Cantidad: {self.cantidad}"


class MovimientoInventario(models.Model):
    TIPO_CHOICES = [
        ('VENTA', 'Venta'),
        ('COMPRA', 'Compra'),
        ('AJUSTE', 'Ajuste'),
        ('MERMA', 'Merma'),
    ]

    negocio = models.CharField(max_length=150)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    lote = models.ForeignKey(Lote, on_delete=models.CASCADE, null=True, blank=True)
    tipo_movimiento = models.CharField(max_length=20, choices=TIPO_CHOICES)
    cantidad = models.IntegerField()  # Puede ser negativo o positivo
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # Apunta al modelo Usuario
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    comentario = models.TextField(blank=True)
    fecha_movimiento = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.tipo_movimiento} - {self.producto.nombre} ({self.cantidad})"

    def save(self, *args, **kwargs):
        """
        Al guardar un movimiento, actualiza el lote correspondiente (si existe)
        y controla si se permite stock negativo o no.
        """
        super().save(*args, **kwargs)  # Guardar primero para tener el ID

        if self.lote:
            lote = self.lote
            nuevo_stock = lote.cantidad

            if self.tipo_movimiento in ['VENTA', 'MERMA']:
                nuevo_stock -= self.cantidad
            elif self.tipo_movimiento in ['COMPRA', 'AJUSTE']:
                nuevo_stock += self.cantidad

            # Verificar si se permite stock negativo
            if not self.producto.permitir_stock_negativo and nuevo_stock < 0:
                # En caso de que no se permita, forzamos a 0 o lanzamos error
                nuevo_stock = 0

            lote.cantidad = nuevo_stock
            lote.save()
