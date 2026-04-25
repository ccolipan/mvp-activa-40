from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Rutina
from .forms import RPEForm

@login_required
def mi_rutina(request):
    # Buscamos la rutina asignada a este usuario que aún no esté completada
    rutina = Rutina.objects.filter(usuario=request.user, completada=False).first()
    
    if request.method == 'POST':
        form = RPEForm(request.POST)
        if form.is_valid():
            # Guardamos la evaluación
            evaluacion = form.save(commit=False)
            evaluacion.rutina = rutina
            evaluacion.save()
            
            # ¡Marcar la rutina como completada!
            rutina.completada = True
            rutina.save()
            return redirect('dashboard')
    else:
        form = RPEForm()

    return render(request, 'rutina_activa.html', {
        'rutina': rutina,
        'form': form
    })
