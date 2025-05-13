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
from django.contrib import messages
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from .forms import PasswordResetRequestForm
from django.contrib.auth.hashers import make_password
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from apps.programas.models import *
from apps.actividades.models import *

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
                if user.is_active:
                    login(request, user)
                    messages.success(request, "Inicio de sesión exitoso")
                    return redirect('inicio')
                else:
                    messages.error(request, "Tu cuenta está desactivada. Contacta al administrador.")
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
def admin_evidencias_points(request, id_usuario):
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

    return render(request, 'admin_dashboard/evidence.html', {
        'puntos': puntos_paginados,
        'query': query,
    })
    
@login_required(login_url='/accounts/login/')
@user_passes_test(is_staff, login_url=('/'))
def profile_superuser(request):
    return render(request, 'admin_dashboard/profile.html')

def solicitar_restauracion(request):
    if request.method == "POST":
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            correo = form.cleaned_data['correo']
            usuario = Usuarios.objects.get(correo=correo)
            
            # Generar un token de recuperación
            token = get_random_string(length=50)
            usuario.password = token  # Temporalmente almacena el token como clave
            usuario.save()

            # Crear enlace de restablecimiento
            reset_link = f"http://127.0.0.1:8000/cambiar_contraseña_confirmar/{token}/"

            # Renderizar la plantilla personalizada con los datos
            mensaje_html = render_to_string("emails/restablecer_contraseña.html", {
                "usuario": usuario,
                "reset_link": reset_link
            })
            mensaje_texto = strip_tags(mensaje_html)  # Versión en texto plano

            # Enviar correo
            send_mail(
                'Restablecer tu contraseña',
                mensaje_texto,
                'noreply@tuapp.com',
                [correo],
                fail_silently=False,
                html_message=mensaje_html  # Mensaje en HTML
            )

            messages.success(request, "Se ha enviado un correo con las instrucciones para restablecer tu contraseña.")
            return redirect('ingresar')
    else:
        form = PasswordResetRequestForm()

    return render(request, 'auth/cambiar_pass.html', {'form': form})

def restablecer_contraseña(request, token):
    try:
        usuario = Usuarios.objects.get(password=token)  # Busca el usuario con el token
    except Usuarios.DoesNotExist:
        messages.error(request, "El enlace no es válido o ha expirado.")
        return redirect('ingresar')

    if request.method == "POST":
        nueva_password = request.POST['nueva_password']
        confirmar_password = request.POST['confirmar_password']

        if nueva_password != confirmar_password:
            messages.error(request, "Las contraseñas no coinciden.")
        else:
            usuario.password = make_password(nueva_password)  # Guarda la nueva contraseña hasheada
            usuario.save()
            messages.success(request, "Tu contraseña ha sido restablecida correctamente.")
            return redirect('ingresar')

    return render(request, 'auth/cambiar_pass_confirmar.html', {'token': token})