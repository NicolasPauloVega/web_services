# Generated by Django 5.1.7 on 2025-03-10 00:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='usuarios',
            options={'verbose_name': 'Usuario', 'verbose_name_plural': 'Usuarios'},
        ),
        migrations.AddField(
            model_name='usuarios',
            name='avatar',
            field=models.FileField(blank=True, null=True, upload_to='usuarios/', verbose_name='Avatar'),
        ),
    ]
