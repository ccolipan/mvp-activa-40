from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from triage.models import Usuario_Restriccion
from entrenamiento.models import Rutina, Alerta_Inactividad, Evaluacion_PostSesion

# Obtenemos el modelo de usuario configurado en el proyecto
Usuario = get_user_model()

def inicio(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'index.html')

@login_required 
def dashboard(request):
    context = {}
    
    if request.user.es_coach:
        # Filtramos alertas de los clientes que tienen asignado a este Coach y estan pendientes
        context['alertas'] = Alerta_Inactividad.objects.filter(
            usuario__coach_asignado=request.user, 
            estado_alerta='pendiente'
        )
        context['rutinas_activas'] = Rutina.objects.filter(coach=request.user, completada=False)
        context['evaluaciones'] = Evaluacion_PostSesion.objects.filter(
            rutina__coach=request.user
        ).order_by('-fecha_evaluacion')[:5]
        
        # NUEVA CONSULTA: Obtener los usuarios registrados cuyo coach asignado sea el usuario en sesion
        context['clientes_asignados'] = Usuario.objects.filter(coach_asignado=request.user)
        
    elif request.user.es_cliente:
        # Si es cliente, enviamos sus restricciones y rutinas activas
        context['mis_restricciones'] = Usuario_Restriccion.objects.filter(usuario=request.user)
        context['mis_rutinas'] = Rutina.objects.filter(usuario=request.user, completada=False)
        
    return render(request, 'dashboard.html', context)