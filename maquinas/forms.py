from django import forms

from .models import Alerta, Parada


class AlertaForm(forms.ModelForm):
    class Meta:
        model = Alerta
        fields = ['maquina', 'descripcion']


class ParadaForm(forms.ModelForm):
    class Meta:
        model = Parada
        fields = ['maquina', 'inicio', 'fin', 'motivo']
        widgets = {
            'inicio': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'fin': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }


class CancelarParadaForm(forms.Form):
    motivo_cancelacion = forms.CharField()
