from django import forms
from .models import Puntos, Actividad, Programa

class PuntosForm(forms.ModelForm):
    class Meta:
        model = Puntos
        fields = '__all__'
        widgets = {
            'evidencia': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }