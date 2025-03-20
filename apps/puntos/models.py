from django.db import models
from django.utils.timezone import now
# Apps models
from apps.usuarios.models import *
from apps.actividades.models import *
from apps.programas.models import *

class Puntos(models.Model):
    usuario = models.ForeignKey(Usuarios, on_delete=models.CASCADE, related_name="Usuarios")
    programa = models.ForeignKey(Programa, on_delete=models.CASCADE, related_name="Programas")
    actividad = models.ForeignKey(Actividad, on_delete=models.CASCADE, related_name="Actividades")
    fecha = models.DateField("Fecha", auto_now_add=True)
    puntos = models.FloatField("Puntos", default=1000)
    evidencia = models.ImageField("Evidencias", upload_to="evidencia/", null=True, blank=True)
    
    class Meta:
        verbose_name = "Punto"
        verbose_name_plural = "Puntos"
    
    def __str__(self):
        return f'{self.usuario.nombres} {self.usuario.apellidos} - {self.puntos}'