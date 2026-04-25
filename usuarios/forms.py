from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from triage.models import Restriccion_Fisica, Usuario_Restriccion

Usuario = get_user_model()

class RegistroClienteForm(UserCreationForm):
    # 1. Nivel de actividad actual
    NIVELES_ACTIVIDAD = [
        ('sedentario', 'Sedentario (Poca o nula actividad)'),
        ('ligero', 'Ligero (1-2 días por semana)'),
        ('moderado', 'Moderado (3-4 días por semana)'),
        ('activo', 'Activo (5+ días por semana)'),
    ]
    nivel_actividad = forms.ChoiceField(
        choices=NIVELES_ACTIVIDAD, 
        label="Nivel de actividad actual",
        widget=forms.Select(attrs={'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-activa-blue outline-none bg-white'})
    )

    # 2. Zonas afectadas (Traídas directamente de tu base de datos del Triage)
    zona_afectada = forms.ModelChoiceField(
        queryset=Restriccion_Fisica.objects.all(),
        required=False,
        empty_label="No tengo ninguna molestia",
        label="Zona anatómica afectada",
        widget=forms.Select(attrs={'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-activa-blue outline-none bg-white'})
    )

    # 3. Escala EVA (Slider)
    nivel_dolor_eva = forms.IntegerField(
        required=False,
        initial=0,
        label="Nivel de molestia (Escala EVA 0-10)",
        widget=forms.NumberInput(attrs={
            'type': 'range', 
            'min': '0', 
            'max': '10', 
            'step': '1', 
            'class': 'w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-activa-accent mt-2',
            'oninput': 'document.getElementById("eva-output").textContent = this.value'
        })
    )

    class Meta(UserCreationForm.Meta):
        model = Usuario
        # Pedimos los datos básicos de registro
        fields = UserCreationForm.Meta.fields + ('first_name', 'email')
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Aplicamos Tailwind a todos los campos de texto y contraseñas
        for field in self.fields:
            if field not in ['nivel_actividad', 'zona_afectada', 'nivel_dolor_eva']:
                self.fields[field].widget.attrs.update({
                    'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-activa-blue outline-none bg-white'
                })