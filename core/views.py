from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

def inicio(request):
    # Si el usuario ya está logueado, se va a su panel privado
    if request.user.is_authenticated:
        return redirect('dashboard')
        
    # Si es un visitante nuevo, le mostramos la landing page (index.html)
    return render(request, 'index.html')

@login_required 
def dashboard(request):
    return render(request, 'dashboard.html')