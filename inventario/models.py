from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
class Negocio(models.Model):
    nombre = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    negocio = models.ForeignKey(Negocio, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=255)
    tipo_producto = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True, null=True)
    precio_compra = models.DecimalField(max_digits=10, decimal_places=2)
    precio_venta = models.DecimalField(max_digits=10, decimal_places=2)
    stock_actual = models.DecimalField(max_digits=10, decimal_places=2)
    stock_minimo = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nombre} - {self.negocio.nombre}"
    
    


class MovimientoInventario(models.Model):
    negocio = models.ForeignKey(Negocio, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    tipo = models.CharField(choices=[('entrada', 'Entrada'), ('salida', 'Salida')], max_length=10)
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    usuario = models.ForeignKey('usuarios.Usuario', on_delete=models.SET_NULL, null=True)
    fecha_movimiento = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.tipo == 'salida' and self.producto.stock_actual < self.cantidad:
            raise ValueError("No hay suficiente stock disponible.")

        # Actualizar stock del producto
        if self.tipo == 'entrada':
            self.producto.stock_actual += self.cantidad
        elif self.tipo == 'salida':
            self.producto.stock_actual -= self.cantidad

        self.producto.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.tipo} - {self.producto.nombre} ({self.cantidad})"


# 🚀 Automatizar ingresos y egresos después de un movimiento de inventario
@receiver(post_save, sender=MovimientoInventario)
def generar_ingreso_egreso(sender, instance, created, **kwargs):
    if created:  # Solo ejecutamos esto cuando se crea un nuevo movimiento
        from finanzas.models import IngresoEgreso
        
        if instance.tipo == 'salida':  # Venta -> Ingreso
            IngresoEgreso.objects.create(
                negocio=instance.negocio,
                tipo='ingreso',
                monto=instance.cantidad * instance.producto.precio_venta,
                usuario=instance.usuario,
                movimiento_inventario=instance
            )
        elif instance.tipo == 'entrada':  # Compra -> Egreso
            IngresoEgreso.objects.create(
                negocio=instance.negocio,
                tipo='egreso',
                monto=instance.cantidad * instance.producto.precio_compra,
                usuario=instance.usuario,
                movimiento_inventario=instance
            )


class Proveedor(models.Model):
    negocio = models.ForeignKey(Negocio, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=255)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    correo = models.EmailField(blank=True, null=True)
    direccion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre


def actualizar_stock(self):
    if self.tipo == 'entrada':
        self.producto.stock_actual += self.cantidad
    elif self.tipo == 'salida':
        self.producto.stock_actual -= self.cantidad

    self.producto.save()



def save(self, *args, **kwargs):
    if self.tipo == 'salida' and self.producto.stock_actual < self.cantidad:
        raise ValueError("No hay suficiente stock disponible.")

    self.actualizar_stock()
    super().save(*args, **kwargs)
