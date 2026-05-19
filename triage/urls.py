from django.urls import path
from . import views

urlpatterns = [
    path('nuevo/', views.registrar_triage, name='registrar_triage'),
    path('coach/ejercicios/nuevo/', views.añadir_ejercicio, name='añadir_ejercicio'),
]