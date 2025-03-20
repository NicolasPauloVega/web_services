from django.urls import path
from .views import *
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', login_required(actividades), name="actividades"),
    path('crear_actividad/', login_required(crearActividad), name="crear_actividad"),
    path('eliminar_actividad/<int:id_actividad>/', login_required(eliminarActividad), name="eliminar_actividad"),
    path('actualizar_actividad/<int:id_actividad>/', login_required(actualizarActividad), name="actualiza_actividad"),
]
