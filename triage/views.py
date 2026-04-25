from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import TriageForm

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
