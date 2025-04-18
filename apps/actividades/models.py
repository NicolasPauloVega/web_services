from django.db import models
from apps.programas.models import Programa

class Actividad(models.Model):
    nombre = models.CharField('Nombre de la actividad', max_length=150)
    puntos = models.FloatField('Puntos (+/-)')
    programa = models.ForeignKey(Programa, on_delete=models.CASCADE, related_name='actividades')
    
    class Meta:
        verbose_name = "Actividad"
        verbose_name_plural = "Actividades"
        
    def __str__(self):
        return f'{ self.nombre } - { self.puntos }'