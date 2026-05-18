from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario

class CustomUsuarioAdmin(UserAdmin):
    model = Usuario
    # Aquí le decimos a Django que muestre nuestras nuevas columnas, ordenadas por categorías
    fieldsets = UserAdmin.fieldsets + (
        ('Roles Activa+40', {
            'fields': ('es_cliente', 'es_coach')
        }),
        ('Identidad y Contacto', {
            'fields': ('fecha_nacimiento', 'telefono')
        }),
        ('Personalización del Entrenamiento', {
            'fields': ('tiempo_disponible', 'objetivo_principal', 'lugar_entrenamiento')
        }),
        ('Seguridad Clínica', {
            'fields': ('lesion_previa', 'descripcion_lesion', 'acepta_terminos')
        }),
        ('Seguimiento y Matchmaking', {
            'fields': ('estado_cliente', 'requiere_revision', 'coach_asignado')
        }),
    )

# Registramos el modelo con esta nueva configuración
admin.site.register(Usuario, CustomUsuarioAdmin)