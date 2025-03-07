# inventario/admin.py
# inventario/apps.py
from django.apps import AppConfig

class InventarioConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'inventario'

    def ready(self):
        # Aquí podrías importar señales (signals) si las tuvieras, 
        # pero no importes los modelos en el nivel del módulo.
        pass
