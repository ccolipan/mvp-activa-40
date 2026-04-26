from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from datetime import date
from triage.models import Restriccion_Fisica
from .models import Usuario

# ==========================================
# 1. FORMULARIO DEL CLIENTE (+40)
# ==========================================
class RegistroClienteForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Usuario
        fields = UserCreationForm.Meta.fields + (
            'first_name', 'last_name', 'email', 'telefono', 'fecha_nacimiento',
            'tiempo_disponible', 'objetivo_principal', 'lugar_entrenamiento',
            'lesion_previa', 'descripcion_lesion', 'acepta_terminos'
        )
        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date'}),
            'descripcion_lesion': forms.Textarea(attrs={'rows': 2}),
        }

    # -- Campos del Triage --
    NIVELES_ACTIVIDAD = [
        ('sedentario', 'Sedentario (Poca o nula actividad)'),
        ('ligero', 'Ligero (1-2 días por semana)'),
        ('moderado', 'Moderado (3-4 días por semana)'),
        ('activo', 'Activo (5+ días por semana)'),
    ]
    nivel_actividad = forms.ChoiceField(choices=NIVELES_ACTIVIDAD, label="Nivel de actividad actual")

    zona_afectada = forms.ModelChoiceField(
        queryset=Restriccion_Fisica.objects.all(),
        required=False,
        empty_label="No tengo ninguna molestia",
        label="Zona anatómica afectada"
    )

    nivel_dolor_eva = forms.IntegerField(
        required=False,
        initial=0,
        label="Nivel de molestia (Escala EVA 0-10)",
        widget=forms.NumberInput(attrs={'type': 'range', 'min': '0', 'max': '10', 'step': '1'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name not in ['nivel_dolor_eva', 'lesion_previa', 'acepta_terminos']:
                field.widget.attrs.update({
                    'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-activa-blue outline-none bg-white'
                })
            elif field_name in ['lesion_previa', 'acepta_terminos']:
                field.widget.attrs.update({
                    'class': 'w-5 h-5 text-activa-blue border-gray-300 rounded focus:ring-activa-blue'
                })
            
            if field_name == 'acepta_terminos':
                field.required = True

    # Validación de Edad (+40)
    def clean_fecha_nacimiento(self):
        fecha_nac = self.cleaned_data.get('fecha_nacimiento')
        if not fecha_nac:
            raise ValidationError("La fecha de nacimiento es obligatoria.")
        
        hoy = date.today()
        edad = hoy.year - fecha_nac.year - ((hoy.month, hoy.day) < (fecha_nac.month, fecha_nac.day))
        
        if edad < 40:
            raise ValidationError(f"Lo sentimos. Activa+40 es exclusivo para mayores de 40 años. Tu edad calculada es {edad} años.")
        
        return fecha_nac

# ==========================================
# 2. FORMULARIO DEL COACH
# ==========================================
class RegistroCoachForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Usuario
        fields = UserCreationForm.Meta.fields + ('first_name','last_name', 'email', 'acepta_terminos')
        
def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name != 'acepta_terminos':
                field.widget.attrs.update({
                    'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-gray-800 outline-none bg-white'
                })
            else:
                field.widget.attrs.update({
                    'class': 'w-5 h-5 text-gray-800 border-gray-300 rounded focus:ring-gray-800'
                })
                field.required = True
