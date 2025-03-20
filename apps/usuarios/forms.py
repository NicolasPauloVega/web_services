from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import Usuarios

class FormularioLogin(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(FormularioLogin, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control form-control-lg'
        self.fields['username'].widget.attrs['placeholder'] = 'Número de documento'
        self.fields['password'].widget.attrs['class'] = 'form-control form-control-lg'
        self.fields['password'].widget.attrs['placeholder'] = 'Contraseña'
        self.fields['password'].widget.attrs['id'] = 'password'
        
class UsuarioRegisterForm(UserCreationForm):
    avatar = forms.FileField(required=False)
    is_staff = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    is_active = forms.BooleanField(required=False, initial=True, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    
    class Meta:
        model = Usuarios
        fields = ['avatar', 'numero_documento', 'nombres', 'apellidos', 'correo', 'password1', 'password2']
        widgets = {
            'numero_documento': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Número de documento'}),
            'nombres': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombres'}),
            'apellidos': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellidos'}),
            'correo': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Correo electrónico'}), 
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Contraseña', 'id': 'password1'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Confirmar contraseña', 'id': 'password2'})
        
        self.fields['avatar'].widget.attrs.update({'class': 'form-control'})
        
    def clean_numero_documento(self):
        numero_documento = self.cleaned_data.get('numero_documento')
        if Usuarios.objects.filter(numero_documento=numero_documento).exists():
            raise forms.ValidationError('Este numero de documento ya existe')
        return numero_documento
    
    def clean_correo(self):
        correo = self.cleaned_data.get('correo')
        if Usuarios.objects.filter(correo=correo).exists():
            raise forms.ValidationError('Esta direccion de correo electronico ya existe')
        return correo
    
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Las contraseñas no coinciden.")
        
        return password2
    
class UsuarioUpdateForm(forms.ModelForm):
    class Meta:
        model = Usuarios
        fields = ['avatar', 'numero_documento', 'nombres', 'apellidos', 'correo', 'is_staff', 'is_active']
        
        widgets = {
            'avatar': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'numero_documento': forms.NumberInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),  # No editable
            'nombres': forms.TextInput(attrs={'class': 'form-control'}),
            'apellidos': forms.TextInput(attrs={'class': 'form-control'}),
            'correo': forms.EmailInput(attrs={'class': 'form-control'}),
            'is_staff': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean_numero_documento(self):
        """Evita que el usuario modifique su número de documento"""
        return self.instance.numero_documento  # Retorna el valor actual sin cambios