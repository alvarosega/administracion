from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class UsuarioManager(BaseUserManager):
    def create_user(self, username, email, password=None, rol='empleado', negocio=None):
        if not email:
            raise ValueError("El usuario debe tener un correo electrónico.")

        email = self.normalize_email(email)
        user = self.model(username=username, email=email, rol=rol, negocio=negocio)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password):
        return self.create_user(username, email, password, rol='admin')

class Usuario(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    
    # Relación con el modelo de negocio
    negocio = models.ForeignKey('inventario.Negocio', on_delete=models.CASCADE, null=True, blank=True)

    ROL_CHOICES = [
        ('admin', 'Administrador'),
        ('empleado', 'Empleado'),
    ]
    rol = models.CharField(max_length=15, choices=ROL_CHOICES, default='empleado')

    is_active = models.BooleanField(default=True)  # Permite activar/desactivar usuarios
    is_staff = models.BooleanField(default=False)  # Bloquea el acceso al panel de Django Admin

    objects = UsuarioManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return f"{self.username} - {self.negocio.nombre if self.negocio else 'Sin negocio'}"

    @property
    def es_admin(self):
        return self.rol == 'admin'
