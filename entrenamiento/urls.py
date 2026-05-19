from django.urls import path
from . import views

app_name = 'entrenamiento'

urlpatterns = [
    # Ruta existente para el cliente
    path('activa/', views.mi_rutina, name='mi_rutina'),
    
    # Nueva ruta para el portal del coach
    path('coach/crear-rutina/', views.crear_rutina_coach, name='crear_rutina_coach'),

    # Nueva ruta para el cliente
    path('mi-rutina/', views.mi_rutina, name='mi_rutina')
]