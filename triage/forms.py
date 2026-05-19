from django import forms
from .models import Usuario_Restriccion, Ejercicio

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
# Formulario para el coach
class EjercicioForm(forms.ModelForm):
    class Meta:
        model = Ejercicio
        fields = ['nombre', 'grupo_muscular']
        labels = {
            'nombre': 'Nombre del Ejercicio',
            'grupo_muscular': 'Grupo Muscular Objetivo'
        }
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-blue-500 outline-none', 'placeholder': 'Ej: Sentadillas Goblet'}),
            'grupo_muscular': forms.TextInput(attrs={'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-blue-500 outline-none', 'placeholder': 'Ej: Cuádriceps'}),
        }