# Generated by Django 5.1.7 on 2025-03-11 21:38

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('actividades', '0001_initial'),
        ('programas', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Puntos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField(default=django.utils.timezone.now, verbose_name='Fecha')),
                ('puntos', models.FloatField(default=1000, verbose_name='Puntos')),
                ('evidencia', models.ImageField(blank=True, null=True, upload_to='evidencia/', verbose_name='Evidencias')),
                ('actividad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Actividades', to='actividades.actividad')),
                ('programa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Programas', to='programas.programa')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Usuarios', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Punto',
                'verbose_name_plural': 'Puntos',
            },
        ),
    ]
