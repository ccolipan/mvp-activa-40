from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Rutina
from .forms import RPEForm, RutinaForm, RutinaDetalleFormSet
from django.contrib import messages

@login_required
def mi_rutina(request):
    # Seguridad: Solo clientes pueden ver esto
    if not getattr(request.user, 'es_cliente', False):
        return redirect('dashboard')

    # Buscamos la rutina asignada optimizando la carga de ejercicios con prefetch_related
    rutina = Rutina.objects.filter(usuario=request.user, completada=False).prefetch_related('detalles__ejercicio').first()
    
    if not rutina:
        messages.info(request, 'No tienes rutinas pendientes.')
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = RPEForm(request.POST)
        if form.is_valid():
            # Guardamos la evaluacion
            evaluacion = form.save(commit=False)
            evaluacion.rutina = rutina
            evaluacion.save()
            
            # Marcar la rutina como completada
            rutina.completada = True
            rutina.save()
            messages.success(request, '¡Felicidades! Has completado tu entrenamiento de hoy.')
            return redirect('dashboard')
    else:
        form = RPEForm()

    return render(request, 'entrenamiento/rutina_activa.html', {
        'rutina': rutina,
        'form': form
    })

@login_required
def crear_rutina_coach(request):
    # Validacion de seguridad: Solo el coach puede acceder
    if not getattr(request.user, 'es_coach', False):
        return redirect('dashboard')

    if request.method == 'POST':
        # Se inyecta el usuario actual (coach) para procesar los datos y filtrar clientes
        form_rutina = RutinaForm(request.POST, coach=request.user)
        
        if form_rutina.is_valid():
            rutina = form_rutina.save(commit=False)
            # Asignacion automatica del coach para trazabilidad
            rutina.coach = request.user
            # Guardamos el padre en la base de datos para generar su Primary Key
            rutina.save()
            
            # Vinculamos los detalles (ejercicios) a la rutina recien creada
            formset_detalles = RutinaDetalleFormSet(request.POST, instance=rutina)
            
            if formset_detalles.is_valid():
                formset_detalles.save()
                messages.success(request, 'Rutina asignada al usuario de forma exitosa.')
                return redirect('dashboard')
            else:
                # Rollback de seguridad: Si los ejercicios fallan, eliminamos la rutina huerfana
                rutina.delete()
    else:
        # Peticion GET: Se inicializan los formularios vacios
        form_rutina = RutinaForm(coach=request.user)
        formset_detalles = RutinaDetalleFormSet()

    contexto = {
        'form_rutina': form_rutina,
        'formset_detalles': formset_detalles,
    }
    
    return render(request, 'entrenamiento/crear_rutina.html', contexto)
