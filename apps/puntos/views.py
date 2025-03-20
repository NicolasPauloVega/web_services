from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Usuarios, Programa, Actividad, Puntos
from .forms import PuntosForm
from django.http import JsonResponse
from django.contrib.auth.decorators import user_passes_test, login_required

def is_staff(user):
    return user.is_active and user.is_staff # Validar si es administrador y esta activo

@login_required(login_url='/accounts/login/')
@user_passes_test(is_staff, login_url='/')
def obtener_actividades(request, programa_id):
    actividades = Actividad.objects.filter(programa_id=programa_id).values("id", "nombre", "puntos")
    return JsonResponse(list(actividades), safe=False)

@login_required(login_url='/accounts/login/')
@user_passes_test(is_staff, login_url='/')
def puntos(request, id_usuario):
    usuario = Usuarios.objects.get(numero_documento=id_usuario)
    programas = Programa.objects.all()
    actividades = Actividad.objects.none()  # Inicialmente vacío
    form = PuntosForm()

    if request.method == 'POST':
        programa_id = request.POST.get('programa')  
        actividad_id = request.POST.get('actividad')
        puntos = int(request.POST.get('puntos', 0))
        
        if programa_id:
            actividades = Actividad.objects.filter(programa_id=programa_id)

        if puntos < 0 and usuario.puntos_totales + puntos < 0:
            messages.error(request, 'No puedes restar más puntos de los que tiene el usuario.')
        else:
            usuario.puntos_totales += puntos  # Sumar o restar según el valor de puntos
            usuario.save()

            form = PuntosForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                messages.success(request, '¡Los puntos fueron asignados con éxito!')
                return redirect('puntos', id_usuario=id_usuario)
            else:
                messages.error(request, '¡Hubo un error al asignar los puntos!')

    return render(request, 'puntos.html', {
        'usuario': usuario,
        'programas': programas,
        'actividades': actividades,
        'form': form
    })

@login_required(login_url='/accounts/login/')
@user_passes_test(is_staff, login_url='/')
def puntos_evidencia(request, id_usuario):
    puntos = Puntos.objects.filter(usuario=id_usuario)
    return render(request, 'evidencias.html', {'evidencias': puntos})

@login_required(login_url='/accounts/login/')
@user_passes_test(is_staff, login_url='/')
def estadistica(request):
    usuarios = Usuarios.objects.values('nombres', 'apellidos', 'puntos_totales')

    if not usuarios:  # Si no hay usuarios, devolver datos vacíos
        return JsonResponse({"error": "No hay usuarios registrados"}, status=400)

    mejor_usuario = max(usuarios, key=lambda x: x['puntos_totales'])
    peor_usuario = min(usuarios, key=lambda x: x['puntos_totales'])

    data = {
        "mejor": {
            "nombre": mejor_usuario['nombres'],
            "apellidos": mejor_usuario['apellidos'],
            "puntos": mejor_usuario['puntos_totales']
        },
        "peor": {
            "nombre": peor_usuario['nombres'],
            "apellidos": peor_usuario['apellidos'],
            "puntos": peor_usuario['puntos_totales']
        },
        "todos": [
            {"nombre": usuario['nombres'], "apellidos": usuario['apellidos'], "puntos": usuario['puntos_totales']}
            for usuario in usuarios
        ]
    }

    return JsonResponse(data)

@user_passes_test(is_staff)
def estadisticas_views(request):
    return render(request, 'estadisticas.html')