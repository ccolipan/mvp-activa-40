from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from triage.models import Usuario_Restriccion
from entrenamiento.models import Rutina, Alerta_Inactividad

def inicio(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'index.html')

@login_required 
def dashboard(request):
    # Creamos un diccionario vacío para enviar datos al HTML
    context = {}
    
    if request.user.es_coach:
        # Si es coach, le mandamos las alertas pendientes
        context['alertas'] = Alerta_Inactividad.objects.filter(resuelta=False)
        context['rutinas_activas'] = Rutina.objects.filter(coach=request.user, completada=False)
        
    elif request.user.es_cliente:
        # Si es cliente, le mandamos sus dolores registrados y su rutina
        context['mis_restricciones'] = Usuario_Restriccion.objects.filter(usuario=request.user)
        context['mis_rutinas'] = Rutina.objects.filter(usuario=request.user, completada=False)
        
    # Le pasamos el contexto a la plantilla
    return render(request, 'dashboard.html', context)