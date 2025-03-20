from django import forms
from .models import *

class FormActividades(forms.ModelForm):
    class Meta:
        model = Actividad
        fields = ['nombre', 'puntos', 'programa']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de la actividad'}),
            'puntos': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Puntos (+/-)'}),
        }
        
class FormActualizarActividad(forms.ModelForm):
    
    programa = forms.ModelChoiceField(
        queryset=Programa.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control', 'readonly': 'readonly'}),
        empty_label=None
    )
    
    class Meta:
        model = Actividad
        fields = ['nombre', 'puntos', 'programa']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre'}),
            'puntos': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Puntos (+/-)'}),
        }