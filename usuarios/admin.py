from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario

class CustomUserAdmin(UserAdmin):
    model = Usuario
    # El panel muestra los campos nuevos
    fieldsets = UserAdmin.fieldsets + (
        ('Perfilamiento Activa+40', {'fields': ('es_cliente', 'es_coach', 'fecha_nacimiento', 'telefono')}),
    )
    # Configuramos qué columnas ver en la lista principal
    list_display = ['username', 'first_name', 'last_name', 'es_cliente', 'es_coach']

admin.site.register(Usuario, CustomUserAdmin)
