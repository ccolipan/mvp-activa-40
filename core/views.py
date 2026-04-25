from django.shortcuts import render

def inicio(request):
    # Esta función renderiza el landing page
    return render(request, 'index.html')