from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):
    # Roles logicos: Diferencian los permisos de acceso y vistas en el ecosistema 
    es_cliente = models.BooleanField(default=False, verbose_name="Es Cliente (+40)")
    es_coach = models.BooleanField(default=False, verbose_name="Es Entrenador")
    
    # Perfilamiento: Parametros criticos para la validación etaria y gestión proactiva
    fecha_nacimiento = models.DateField(null=True, blank=True, verbose_name="Fecha de Nacimiento")
    telefono = models.CharField(max_length=15, null=True, blank=True, verbose_name="Teléfono de contacto")

    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"

    def __str__(self):
        # Etiqueta visual dinamica para el panel de administración
        rol = "Coach" if self.es_coach else "Cliente"
        return f"{self.first_name} {self.last_name} ({rol})"