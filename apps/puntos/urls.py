from django.urls import path
from .views import *
from apps.usuarios.views import reiniciar_puntos
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('usuario/<int:id_usuario>', login_required(puntos), name="puntos"),
    path('obtener_actividades/<int:programa_id>/', login_required(obtener_actividades), name='obtener_actividades'),
    path('evidencias/<int:id_usuario>/', login_required(puntos_evidencia), name="puntos_evidencia"),
    path('datos_graficos/', login_required(estadistica), name="datos_graficos"),
    path('estadisticas/', login_required(estadisticas_views), name="estadisticas"),
    path('reiniciar_puntos/', login_required(reiniciar_puntos), name="reiniciar_puntos"),
    path("exportar-excel/", exportar_excel, name="exportar_excel"),
]
