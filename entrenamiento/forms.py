from django import forms
from .models import Evaluacion_PostSesion

class RPEForm(forms.ModelForm):
    class Meta:
        model = Evaluacion_PostSesion
        fields = ['esfuerzo_rpe', 'comentario_usuario']
        labels = {
            'esfuerzo_rpe': '¿Qué tan intenso fue el entrenamiento de hoy? (RPE 1-10)',
            'comentario_usuario': '¿Algún comentario, molestia o duda para tu Coach?'
        }
        widgets = {
            'esfuerzo_rpe': forms.Select(attrs={'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-activa-blue outline-none bg-white'}),
            'comentario_usuario': forms.Textarea(attrs={'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-activa-blue outline-none', 'rows': 3}),
        }