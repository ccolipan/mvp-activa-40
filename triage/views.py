from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import TriageForm, EjercicioForm

@login_required
def registrar_triage(request):
    if request.method == 'POST':
        # Si el usuario envió el formulario
        form = TriageForm(request.POST)
        if form.is_valid():
            # Guardamos el dato, pero pausamos un segundo (commit=False)
            nuevo_registro = form.save(commit=False)
            # Le asignamos automáticamente el usuario que está logueado
            nuevo_registro.usuario = request.user
            nuevo_registro.save() # Ahora sí guardamos en la base de datos
            return redirect('dashboard') # Lo devolvemos al panel
    else:
        # Si recién entra a la página, le mostramos el formulario vacío
        form = TriageForm()
        
    return render(request, 'triage_form.html', {'form': form})

# Vista para que el coach guarde los ejercicios
@login_required
def añadir_ejercicio(request):
    # Validamos por seguridad que solo un coach acceda a esta ruta
    if not getattr(request.user, 'es_coach', False):
        return redirect('dashboard')

    if request.method == 'POST':
        form = EjercicioForm(request.POST)
        if form.is_valid():
            form.save()
            # Este mensaje lo atrapará el rectángulo verde que ya configuramos en el dashboard
            messages.success(request, 'Ejercicio añadido al catálogo correctamente.')
            return redirect('dashboard')
    else:
        form = EjercicioForm()

    return render(request, 'entrenamiento/añadir_ejercicio.html', {'form': form})