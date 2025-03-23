from django.urls import path, include
from .views import *
from apps.puntos.views import *
from django.contrib.auth.decorators import login_required

urlpatterns = [
    # Visualización de usuarios
    path('', login_required(inicio), name="inicio"),
    # Validacion de usuarios
    path('accounts/login/', ingresar, name="ingresar"),
    path('accounts/logout/', login_required(salir), name="salir"),
    path('accounts/register/', login_required(registro), name="registrar"),
    # Perfil de usuario
    path('perfil_usuario/<int:id_usuario>', login_required(profile), name="perfil"),
    # Evidencias de usuario
    path('evidencias/<int:id_usuario>', login_required(evidencias_points), name="puntos"),
    # Administración
    path('admin_panel/', login_required(admin_dashboard), name="admin_panel"),
    # Administración usuarios
    path('admin_panel/usuarios', login_required(usuarios), name="list_usuarios"),
    path('admin_panel/usuarios/perfil', login_required(profile_superuser), name="profile_superuser"),
    path('admin_panel/crear_usuario', login_required(crear_usuario), name="crear_usuario"),
    path('admin_panel/usuarios/actualizar/<int:id_usuario>', login_required(actualizar_usuarios), name="act_usuario"),
    # Administracion puntos
    path('admin_panel/puntos/', include('apps.puntos.urls')),
    # Administracion programas
    path('admin_panel/programas/', include('apps.programas.urls')),
    # Administración actividades
    path('admin_panel/actividades/', include('apps.actividades.urls')),
]
