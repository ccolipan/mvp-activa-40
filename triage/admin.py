from django.contrib import admin
from .models import Restriccion_Fisica, Ejercicio, Contraindicacion, Usuario_Restriccion

# Registramos las 4 clases de nuestro ecosistema de seguridad
admin.site.register(Restriccion_Fisica)
admin.site.register(Ejercicio)
admin.site.register(Contraindicacion)
admin.site.register(Usuario_Restriccion)