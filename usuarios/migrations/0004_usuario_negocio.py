# Generated by Django 5.1.6 on 2025-03-05 15:17

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("inventario", "0002_initial"),
        ("usuarios", "0003_remove_usuario_negocio_usuario_is_staff"),
    ]

    operations = [
        migrations.AddField(
            model_name="usuario",
            name="negocio",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="inventario.negocio",
            ),
        ),
    ]
