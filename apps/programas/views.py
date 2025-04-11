from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404
from .models import *
from django.db.models import Q
from django.core.paginator import Paginator
from .forms import *
from apps.actividades.models import *
from django.contrib.auth.decorators import user_passes_test, login_required

def is_staff(user):
    return user.is_active and user.is_staff # Validar si es administrador y esta activo

@login_required(login_url='/accounts/login/')
@user_passes_test(is_staff, login_url='/')
def programs(request):
    programas = Programa.objects.all()
    query = request.GET.get('q', '') # Consultar
    
    # Si la consulta es valida
    if query:
        # Buscar al usuario en la bd
        programas = Programa.objects.filter(Q(nombre__icontains=query))
    
    paginator = Paginator(programas,10) # tomar 10 usuarios para paginar
    page_number = request.GET.get('page') # Paginar
    programas_paginados = paginator.get_page(page_number) # Mostrar los usuarios paginados
    return render(request, 'programas.html', {'programas': programas, 'query': query})

@login_required(login_url='/accounts/login/')
@user_passes_test(is_staff, login_url='/')
def crear_programa(request):
    if request.method == 'POST':
        form = FormProgramas(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Programa creado exitosamente!')
            return redirect('crear_programa')
        else:
            messages.error(request, '¡El programa no se pudo crear!')
    else:
        form = FormProgramas()
    return render(request, 'crear_programa.html', {'form': form})

@login_required(login_url='/accounts/login/')
@user_passes_test(is_staff, login_url='/')
def eliminar_programa(request, id_programa):
    programa = get_object_or_404(Programa, id=id_programa)
    programa.delete()
    messages.success(request, 'El programa ha sido eliminado exitosamente')
    return redirect('programas')

@login_required(login_url='/accounts/login/')
@user_passes_test(is_staff, login_url='/')
def actualizar_programa(request, id_programa):
    programa = get_object_or_404(Programa, id=id_programa)
    
    if request.method == 'POST':
        form = FormActualizarPrograma(request.POST, instance=programa)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Se actualizó correctamente la actividad!')
            return redirect('programas')
        else:
            messages.error(request, '¡No se pudo actualizar la actividad!')
    else:
        form = FormActualizarPrograma(instance=programa)

    return render(request, 'update_programas.html', {'form': form, 'programa': programa})