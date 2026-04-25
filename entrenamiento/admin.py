from django.contrib import admin
from .models import Rutina, Detalle_Rutina, Evaluacion_PostSesion, Alerta_Inactividad

admin.site.register(Rutina)
admin.site.register(Detalle_Rutina)
admin.site.register(Evaluacion_PostSesion)
admin.site.register(Alerta_Inactividad)