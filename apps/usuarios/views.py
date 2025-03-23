from django.contrib.auth.decorators import user_passes_test, login_required
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import FormularioLogin, UsuarioRegisterForm, UsuarioUpdateForm
from .models import Usuarios
from apps.puntos.models import Puntos
from django.utils import timezone
from django.db.models import Q
from django.core.paginator import Paginator
from django.utils.timezone import now
from django.http import HttpResponseForbidden

def is_staff(user):
    return user.is_active and user.is_staff # Validar si es administrador y esta activo

def inicio(request):
    usuarios = Usuarios.objects.all().order_by('-puntos_totales')
    query = request.GET.get('q', '') # Consultar
    
    # Si la consulta es valida
    if query:
        # Buscar al usuario en la bd
        usuarios = usuarios.filter(
            Q(numero_documento__icontains = query) |
            Q(nombres__icontains = query) |
            Q(apellidos__icontains = query)
        )
    
    paginator = Paginator(usuarios,10) # tomar 10 usuarios para paginar
    page_number = request.GET.get('page') # Paginar
    usuarios_paginados = paginator.get_page(page_number) # Mostrar los usuarios paginados
    return render(request, 'blog.html', {'usuario': usuarios_paginados, 'query': query})

@login_required(login_url='/accounts/login/')
@user_passes_test(is_staff, login_url='/')
def registro(request):
    if request.method == "POST":
        form = UsuarioRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password1"])
            user.save()
            return redirect('list_usuarios')
    else:
        form = UsuarioRegisterForm()
    return render(request, 'registration/registro.html', {'form': form})

def ingresar(request):
    form = FormularioLogin()
    
    if request.method == 'POST':
        form = FormularioLogin(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            
            # Autenticación de usuario
            user = authenticate(request, username = username, password = password)
            
            if user is not None:
                login(request, user)
                return redirect('inicio')
            else:
                form.add_error(None, "Número de documento o contraseña incorrectos")
        else:
            form = FormularioLogin()
    
    return render(request, 'registration/login.html', {'form': form})

def salir(request):
    logout(request)
    return redirect('ingresar')

@login_required(login_url='/accounts/login/')
@user_passes_test(is_staff, login_url='/')
def reiniciar_puntos():
    hoy = now().date()
    usuarios = Usuarios.objects.all()
    
    for usuario in usuarios:
        if(hoy.year, hoy.month) != (usuario.ultimo_reinicio.year, usuario.ultimo_reinicio.month):
            usuario.puntos_totales = 1000
            usuario.ultimo_reinicio = hoy
            usuario.save()

@login_required(login_url='/accounts/login/')
@user_passes_test(is_staff, login_url='/')
def admin_dashboard(request):
    usuario = Usuarios.objects.all()
    total_usuarios = usuario.count()
    fecha_actual = timezone.now().date() # Fecha actual
    return render(request, 'admin_dashboard/main.html', {
        'usuario':usuario,
        'total_usuarios': total_usuarios,
        'fecha_actual': fecha_actual
        })

@login_required(login_url='/accounts/login/')
@user_passes_test(is_staff, login_url='/')
def usuarios(request):
    usuarios = Usuarios.objects.all()
    query = request.GET.get('q', '') # Consultar
    
    # Si la consulta es valida
    if query:
        # Buscar al usuario en la bd
        usuarios = usuarios.filter(
            Q(numero_documento__icontains = query) |
            Q(nombres__icontains = query) |
            Q(apellidos__icontains = query)
        )
    
    paginator = Paginator(usuarios,10) # tomar 10 usuarios para paginar
    page_number = request.GET.get('page') # Paginar
    usuarios_paginados = paginator.get_page(page_number) # Mostrar los usuarios paginados
    
    return render(request, 'admin_dashboard/usuarios/users.html', {'usuario': usuarios_paginados, 'query': query})

@login_required(login_url='/accounts/login/')
@user_passes_test(is_staff, login_url='/')
def actualizar_usuarios(request, id_usuario):
    usuario = get_object_or_404(Usuarios, numero_documento=id_usuario)

    if request.method == "POST":
        form = UsuarioUpdateForm(request.POST, request.FILES, instance=usuario)
        if form.is_valid():
            form.save()
            return redirect('list_usuarios')  # Cambia esto por la vista donde se listan los usuarios
    else:
        form = UsuarioUpdateForm(instance=usuario)

    return render(request, 'admin_dashboard/usuarios/update.html', {'form': form, 'usuario': usuario})

@login_required(login_url='/accounts/login/')
@user_passes_test(is_staff, login_url='/')
def crear_usuario(request):
    if request.method == "POST":
        form = UsuarioRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password1"])
            user.save()
            messages.success(request, "¡Usuario creado exitosamente!")
            return redirect('list_usuarios')
        else:
            messages.error(request, "Hubo un error al crear el usuario. Verifica los datos ingresados.")

    else:
        form = UsuarioRegisterForm()
    
    return render(request, 'admin_dashboard/usuarios/crear_usuario.html', {'form': form})

@login_required(login_url='/accounts/login')
@user_passes_test(is_staff, login_url='/')
def reiniciar_puntos(request):
    puntos = 1000
    fecha_reinicio = now()
    
    Usuarios.objects.update(puntos_totales=puntos, ultimo_reinicio=fecha_reinicio)
    
    messages.success(request, "¡Puntos reiniciados con éxito!")
    return redirect('list_usuarios')

@login_required(login_url='/accounts/login')
@user_passes_test(is_staff, login_url=('/'))
def profile(request, id_usuario):
    usuario = Usuarios.objects.filter(numero_documento = id_usuario)
    query = request.GET.get('q', '')
    
    if query:
        # Buscar al usuario en la bd
        usuario = usuarios.filter(
            Q(numero_documento__icontains = query) |
            Q(nombres__icontains = query) |
            Q(apellidos__icontains = query)
        )
        
    paginator = Paginator(usuario,10)
    page_number = request.GET.get('page')
    usuarios_paginados = paginator.get_page(page_number)
    return render(request, 'registration/profile.html', {'usuario': usuarios_paginados, 'query': query})

@login_required(login_url='/accounts/login')
@user_passes_test(is_staff, login_url=('/'))
def profile(request, id_usuario):
    usuario = Usuarios.objects.filter(numero_documento = id_usuario)
    query = request.GET.get('q', '')
    
    if query:
        # Buscar al usuario en la bd
        usuario = usuarios.filter(
            Q(numero_documento__icontains = query) |
            Q(nombres__icontains = query) |
            Q(apellidos__icontains = query)
        )
        
    paginator = Paginator(usuario,10)
    page_number = request.GET.get('page')
    usuarios_paginados = paginator.get_page(page_number)
    return render(request, 'registration/profile.html', {'usuario': usuarios_paginados, 'query': query})

@login_required(login_url='/accounts/login/')
def evidencias_points(request, id_usuario):
    puntos = Puntos.objects.filter(usuario=id_usuario)
    query = request.GET.get('q', '')

    if query:
        puntos = puntos.filter(
            Q(programa__nombre__icontains=query) |
            Q(actividad__nombre__icontains=query)
        )

    # Paginación
    paginator = Paginator(puntos, 10)
    page_number = request.GET.get('page')
    puntos_paginados = paginator.get_page(page_number)

    return render(request, 'registration/evidence.html', {
        'puntos': puntos_paginados, 
        'query': query,
    })
    
@login_required(login_url='/accounts/login/')
@user_passes_test(is_staff, login_url=('/'))
def profile_superuser(request):
    return render(request, 'admin_dashboard/profile.html')