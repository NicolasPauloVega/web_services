from django.urls import path
from .views import *
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', login_required(programs), name="programas"),
    path('crear_programa/', login_required(crear_programa), name="crear_programa"),
    path('editar_programa/<int:id_programa>', login_required(actualizar_programa), name="editar_programa"),
    path('eliminar_programa/<int:id_programa>', login_required(eliminar_programa), name="eliminar_programa"),
]
