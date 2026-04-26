from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import RegistroClienteForm, RegistroCoachForm
from triage.models import Usuario_Restriccion

def registro_cliente(request):
    if request.method == 'POST':
        form = RegistroClienteForm(request.POST)
        if form.is_valid():
            usuario = form.save(commit=False)
            usuario.es_cliente = True
            
            # Leemos los datos del triage
            zona = form.cleaned_data.get('zona_afectada')
            dolor = form.cleaned_data.get('nivel_dolor_eva', 0)
            
            # 🔥 LÓGICA DE CONTROL: Si el EVA es 7 o más, requiere revisión manual
            if dolor >= 7:
                usuario.requiere_revision = True
                usuario.estado_cliente = 'pendiente'
            else:
                usuario.estado_cliente = 'activo'
                
            usuario.save() # Guardamos el usuario con sus nuevos campos

            # Guardamos la restricción si existe
            if zona and dolor > 0:
                Usuario_Restriccion.objects.create(
                    usuario=usuario,
                    restriccion=zona,
                    nivel_dolor_eva=dolor
                )
            
            login(request, usuario)
            return redirect('dashboard')
    else:
        form = RegistroClienteForm()
        
    return render(request, 'registro.html', {'form': form})

def registro_coach(request):
    if request.method == 'POST':
        form = RegistroCoachForm(request.POST)
        if form.is_valid():
            usuario = form.save(commit=False)
            #LLave maestra del entrenador
            usuario.es_coach = True 
            usuario.save()
            #Iniciamos sesion y lo mandamos a su panel de control
            login(request, usuario)
            return redirect('dashboard')
    else:
        form = RegistroCoachForm()
        
    return render(request, 'registro_coach.html', {'form': form})