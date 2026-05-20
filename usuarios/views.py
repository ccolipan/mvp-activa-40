from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from .forms import RegistroClienteForm, RegistroCoachForm
from triage.models import Usuario_Restriccion

def registro_cliente(request):
    # CONTROL DE ACCESO: Verificamos si el usuario completo el pago en Transbank
    if not request.session.get('pago_exitoso'):
        messages.warning(request, 'Para completar tu registro, primero debes procesar el pago de la suscripción.')
        return redirect('pagos:resumen')

    if request.method == 'POST':
        form = RegistroClienteForm(request.POST)
        if form.is_valid():
            usuario = form.save(commit=False)
            usuario.es_cliente = True
            
            # Leemos los datos del triage clínico
            zona = form.cleaned_data.get('zona_afectada')
            dolor = form.cleaned_data.get('nivel_dolor_eva', 0)
            
            # LÓGICA DE CONTROL: Si el dolor EVA es 7 o superior, requiere revisión manual del Coach
            if dolor >= 7:
                usuario.requiere_revision = True
                usuario.estado_cliente = 'pendiente'
            else:
                usuario.estado_cliente = 'activo'
                
            usuario.save() # Persistimos el usuario en la base de datos

            # Guardamos la restricción física en el modelo correspondiente si el usuario reportó dolor
            if zona and dolor > 0:
                Usuario_Restriccion.objects.create(
                    usuario=usuario,
                    restriccion=zona,
                    nivel_dolor_eva=dolor
                )
            
            # SEGURIDAD: Limpiamos la variable de sesión para que el ticket de pago no pueda ser reutilizado
            if 'pago_exitoso' in request.session:
                del request.session['pago_exitoso']
            
            login(request, usuario)
            return redirect('dashboard')
    else:
        form = RegistroClienteForm()
        
    return render(request, 'registro.html', {'form': form})


def registro_coach(request):
    # El registro del Coach se mantiene directo e intacto, sin requerir pago
    if request.method == 'POST':
        form = RegistroCoachForm(request.POST)
        if form.is_valid():
            usuario = form.save(commit=False)
            # Llave maestra para definir los permisos del entrenador
            usuario.es_coach = True 
            usuario.save()
            
            # Iniciamos sesión automáticamente y redirigimos al panel de administración
            login(request, usuario)
            return redirect('dashboard')
    else:
        form = RegistroCoachForm()
        
    return render(request, 'registro_coach.html', {'form': form})