from django import forms
from django.forms import inlineformset_factory
from .models import Evaluacion_PostSesion, Rutina, Detalle_Rutina
from django.contrib.auth import get_user_model

Usuario = get_user_model()

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
# Formulario principal para la creacion de la Rutina
class RutinaForm(forms.ModelForm):
    class Meta:
        model = Rutina
        # Se elimina 'estado'. Al crear una rutina solo necesitamos el cliente.
        fields = ['usuario'] 
        labels = {
            'usuario': 'Seleccionar Cliente',
        }
        widgets = {
            'usuario': forms.Select(attrs={'class': 'w-full px-4 py-2 border rounded-lg'})
        }

    def __init__(self, *args, **kwargs):
        # Se extrae el parametro del coach actual para filtrar el listado
        coach_actual = kwargs.pop('coach', None)
        super(RutinaForm, self).__init__(*args, **kwargs)
        
        # Filtra el desplegable para mostrar unicamente los clientes asignados a este coach
        if coach_actual:
            # Corregido a 'coach_asignado' respetando tu modelo
            self.fields['usuario'].queryset = Usuario.objects.filter(coach_asignado=coach_actual)

# Formulario secundario para definir cada ejercicio dentro de la rutina
class DetalleRutinaForm(forms.ModelForm):
    class Meta:
        model = Detalle_Rutina
        fields = ['ejercicio', 'series', 'repeticiones', 'peso_sugerido_kg']
        widgets = {
            'ejercicio': forms.Select(attrs={'class': 'w-full px-2 py-2 border rounded'}),
            'series': forms.NumberInput(attrs={'class': 'w-24 px-2 py-2 border rounded text-center', 'min': '1'}),
            'repeticiones': forms.NumberInput(attrs={'class': 'w-24 px-2 py-2 border rounded text-center', 'min': '1'}),
            'peso_sugerido_kg': forms.NumberInput(attrs={'class': 'w-24 px-2 py-2 border rounded text-center', 'step': '0.5', 'placeholder': 'Ej: 5.0'}),
        }

# Formset que vincula la Rutina con sus Multiples Detalles (Ejercicios)
RutinaDetalleFormSet = inlineformset_factory(
    Rutina, 
    Detalle_Rutina, 
    form=DetalleRutinaForm,
    extra=1,
    can_delete=True
)