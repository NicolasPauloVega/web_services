from django import forms
from .models import *

class FormProgramas(forms.ModelForm):
    class Meta:
        model = Programa
        fields = ['nombre']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del programa'}),
        }