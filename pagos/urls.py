from django.urls import path
from . import views

# Declaración del espacio de nombres de Django requiere para evitar conflictos con otras aplicaciones
app_name = 'pagos'

urlpatterns = [
    path('resumen/', views.resumen_pago, name='resumen'),
    path('iniciar/', views.iniciar_pago, name='iniciar'),
    path('retorno/', views.retorno_pago, name='retorno'),
]