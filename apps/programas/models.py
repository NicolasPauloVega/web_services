from django.db import models

class Programa(models.Model):
    nombre = models.CharField('Programas', max_length=100)
    
    class Meta:
        verbose_name = "Programa"
        verbose_name_plural = "Programas"
        
    def __str__(self):
        return f'{ self.nombre }'