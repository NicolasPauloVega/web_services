from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Usuarios, Programa, Actividad, Puntos
from .forms import PuntosForm
from django.http import JsonResponse
from django.contrib.auth.decorators import user_passes_test, login_required

# Configuraciones excel
from django.http import HttpResponse
from .utils import generar_excel_usuarios

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
    usuarios = list(Usuarios.objects.values('nombres', 'apellidos', 'puntos_totales'))

    if not usuarios:  # Si no hay usuarios, devolver datos vacíos
        return JsonResponse({"error": "No hay usuarios registrados"}, status=400)

    max_puntos = max(usuarios, key=lambda x: x['puntos_totales'])['puntos_totales']
    min_puntos = min(usuarios, key=lambda x: x['puntos_totales'])['puntos_totales']

    mejores_usuarios = [u for u in usuarios if u['puntos_totales'] == max_puntos]
    peores_usuarios = [u for u in usuarios if u['puntos_totales'] == min_puntos]

    data = {
        "mejores": [{"nombre": u['nombres'], "apellidos": u['apellidos'], "puntos": u['puntos_totales']} for u in mejores_usuarios],
        "peores": [{"nombre": u['nombres'], "apellidos": u['apellidos'], "puntos": u['puntos_totales']} for u in peores_usuarios],
        "todos": [{"nombre": u['nombres'], "apellidos": u['apellidos'], "puntos": u['puntos_totales']} for u in usuarios]
    }

    return JsonResponse(data)

@login_required(login_url='/accounts/login/')
@user_passes_test(is_staff)
def estadisticas_views(request):
    return render(request, 'estadisticas.html')

@login_required(login_url='/accounts/login')
@user_passes_test(is_staff)
def exportar_excel(request):
    excel_file = generar_excel_usuarios()
    if not excel_file:
        return HttpResponse("No hay datos para exportar.", content_type="text/plain")

    response = HttpResponse(
        excel_file,
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename="estadisticas_usuarios.xlsx"'
    return response