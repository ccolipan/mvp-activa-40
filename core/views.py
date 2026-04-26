from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from triage.models import Usuario_Restriccion
from entrenamiento.models import Rutina, Alerta_Inactividad, Evaluacion_PostSesion

def inicio(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'index.html')

@login_required 
def dashboard(request):
    # Creamos un diccionario vacío para enviar datos al HTML
    context = {}
    
    if request.user.es_coach:
        # Filtramos alertas SOLO de los clientes que tienen asignado a este Coach, y que estén Pendientes
        context['alertas'] = Alerta_Inactividad.objects.filter(
            usuario__coach_asignado=request.user, 
            estado_alerta='pendiente'
        )
        context['rutinas_activas'] = Rutina.objects.filter(coach=request.user, completada=False)
        context['evaluaciones'] = Evaluacion_PostSesion.objects.filter(
            rutina__coach=request.user
        ).order_by('-fecha_evaluacion')[:5]
        
    elif request.user.es_cliente:
        # Si es cliente, le mandamos sus dolores registrados y su rutina
        context['mis_restricciones'] = Usuario_Restriccion.objects.filter(usuario=request.user)
        context['mis_rutinas'] = Rutina.objects.filter(usuario=request.user, completada=False)
        
    # Le pasamos el contexto a la plantilla
    return render(request, 'dashboard.html', context)