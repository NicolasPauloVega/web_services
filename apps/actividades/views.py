from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from apps.programas.models import Programa
from .forms import FormActividades, FormActualizarActividad
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.decorators import user_passes_test, login_required

def is_staff(user):
    return user.is_active and user.is_staff # Validar si es administrador y esta activo

@login_required(login_url='/accounts/login/')
@user_passes_test(is_staff, login_url='/')
def actividades(request):
    actividades = Actividad.objects.all()
    query = request.GET.get('q', '') # Consulta
    
    if query:
        # buscar la actividad
        actividades = Actividad.objects.filter(
            Q(nombre__icontains=query)
        )
        
    paginator = Paginator(actividades, 10)
    page_number = request.GET.get('page')
    actividades_paginados = paginator.get_page(page_number)
    return render(request, 'actividades.html', {'actividades': actividades_paginados, 'query': query})

@login_required(login_url='/accounts/login/')
@user_passes_test(is_staff, login_url='/')
def crearActividad(request):
    programa = Programa.objects.all()
    form = FormActividades()

    if request.method == 'POST':
        form = FormActividades(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '¡La actividad fue creada exitosamente!')
        else:
            messages.error(request, '¡Hubo un error al crear la actividad!')
    else:
        form = FormActividades()
    return render(request, 'crear_actividad.html', {'programas': programa, 'form': form})

@login_required(login_url='/accounts/login/')
@user_passes_test(is_staff, login_url='/')
def eliminarActividad(request, id_actividad):
    actividad = get_object_or_404(Actividad, id = id_actividad)
    actividad.delete()
    messages.success(request, '¡Actividad eliminada exitosamente!')
    return redirect('actividades')

@login_required(login_url='/accounts/login/')
@user_passes_test(is_staff, login_url='/')
def actualizarActividad(request, id_actividad):
    actividad = get_object_or_404(Actividad, id=id_actividad)
    
    if request.method == 'POST':
        form = FormActualizarActividad(request.POST, instance=actividad)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Se actualizó correctamente la actividad!')
            return redirect('actividades')
        else:
            messages.error(request, '¡No se pudo actualizar la actividad!')
    else:
        form = FormActualizarActividad(instance=actividad)

    return render(request, 'update_actividad.html', {'form': form, 'actividad': actividad})