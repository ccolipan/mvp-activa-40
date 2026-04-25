from django import forms
from .models import Usuario_Restriccion

class TriageForm(forms.ModelForm):
    class Meta:
        model = Usuario_Restriccion
        fields = ['restriccion', 'nivel_dolor_eva']
        labels = {
            'restriccion': '¿Qué zona física te presenta molestias o dolor?',
            'nivel_dolor_eva': 'Del 1 al 10, ¿cuánto dolor sientes? (1=Mínimo, 10=Máximo)'
        }
        widgets = {
            'restriccion': forms.Select(attrs={'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-activa-accent outline-none bg-white'}),
            'nivel_dolor_eva': forms.Select(attrs={'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-activa-accent outline-none bg-white'}),
        }