# Generated by Django 5.1.7 on 2025-04-18 12:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('programas', '0003_alter_programa_descripcion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='programa',
            name='imagen',
            field=models.ImageField(blank=True, null=True, upload_to='programas/'),
        ),
    ]
