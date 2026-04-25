from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import RegistroClienteForm
from triage.models import Usuario_Restriccion

def registro_cliente(request):
    if request.method == 'POST':
        form = RegistroClienteForm(request.POST)
        if form.is_valid():
            # 1. Guardamos al usuario
            usuario = form.save(commit=False)
            usuario.es_cliente = True # Automáticamente es cliente +40
            usuario.save()

            # 2. Si reportó un dolor, lo guardamos en el Triage
            zona = form.cleaned_data.get('zona_afectada')
            dolor = form.cleaned_data.get('nivel_dolor_eva')
            
            if zona and dolor > 0:
                Usuario_Restriccion.objects.create(
                    usuario=usuario,
                    restriccion=zona,
                    nivel_dolor_eva=dolor
                )
            
            # 3. Iniciamos su sesión automáticamente y lo mandamos al Dashboard
            login(request, usuario)
            return redirect('dashboard')
    else:
        form = RegistroClienteForm()
        
    return render(request, 'registro.html', {'form': form})