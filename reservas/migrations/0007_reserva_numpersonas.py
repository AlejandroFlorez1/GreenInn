# Generated by Django 5.0.4 on 2024-05-02 00:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservas', '0006_producto_imagen'),
    ]

    operations = [
        migrations.AddField(
            model_name='reserva',
            name='numPersonas',
            field=models.PositiveIntegerField(default=7, verbose_name='Personas'),
        ),
    ]
