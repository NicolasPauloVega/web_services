from django.contrib import admin
from apps.programas.models import *
from apps.actividades.models import *

# Register your models here.
admin.site.register(Programa)
admin.site.register(Actividad)