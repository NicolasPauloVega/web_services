from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils.timezone import now

class UsuariosManager(BaseUserManager):
    def create_user(self, numero_documento, nombres, apellidos, correo, password=None, **extra_fields):
        if not numero_documento:
            raise ValueError('El usuario debe tener un número de documento')
        if not correo:
            raise ValueError('El usuario debe tener un correo electrónico')

        correo = self.normalize_email(correo)
        user = self.model(
            numero_documento=numero_documento,
            nombres=nombres,
            apellidos=apellidos,
            correo=correo,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, numero_documento, nombres, apellidos, correo, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(numero_documento, nombres, apellidos, correo, password, **extra_fields)

class Usuarios(AbstractBaseUser, PermissionsMixin):
    avatar = models.FileField('Avatar', upload_to='usuarios/', null=True, blank=True)
    nombres = models.CharField('Nombres', max_length=50)
    apellidos = models.CharField('Apellidos', max_length=100)
    numero_documento = models.IntegerField('Número de documento', primary_key=True, unique=True)
    correo = models.EmailField('Correo electrónico', max_length=255, unique=True)
    puntos_totales = models.IntegerField('Número total de puntos', default=1000)
    password = models.CharField('Contraseña', max_length=255)
    ultimo_reinicio = models.DateField('Ultimo reinicio de puntos', default=now) # Reiniciar puntos
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UsuariosManager()

    USERNAME_FIELD = 'numero_documento'
    REQUIRED_FIELDS = ['nombres', 'apellidos', 'correo']

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        
    def __str__(self):
        return f'{self.nombres} {self.apellidos}'
