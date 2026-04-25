from django.urls import path
from . import views

urlpatterns = [
    path('activa/', views.mi_rutina, name='mi_rutina'),
]