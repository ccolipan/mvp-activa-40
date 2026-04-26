from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
    es_cliente = models.BooleanField(default=False)
    es_coach = models.BooleanField(default=False)

    # --- Control de Coach --
    ESTADO_COACH_CHOICES = [
        ('activo', 'Activo'),
        ('inactivo', 'Inactivo'),
    ]
    estado_coach = models.CharField(max_length=20, choices=ESTADO_COACH_CHOICES, default='activo', verbose_name="Estado del Coach")

    # --- IDENTIDAD Y CONTACTO ---
    # El 'last_name' ya viene incluido en AbstractUser, así que no necesitamos crearlo.
    fecha_nacimiento = models.DateField(null=True, blank=True, verbose_name="Fecha de Nacimiento")
    telefono = models.CharField(max_length=20, null=True, blank=True, verbose_name="Teléfono")

    # --- PERSONALIZACIÓN ---
    TIEMPO_CHOICES = [
        ('15', '15 minutos'),
        ('30', '30 minutos'),
        ('45', '45+ minutos'),
    ]
    tiempo_disponible = models.CharField(max_length=10, choices=TIEMPO_CHOICES, null=True, blank=True)
    
    OBJETIVO_CHOICES = [
        ('salud', 'Salud General'),
        ('fuerza', 'Ganar Fuerza'),
        ('movilidad', 'Mejorar Movilidad'),
        ('peso', 'Bajar de Peso'),
    ]
    objetivo_principal = models.CharField(max_length=20, choices=OBJETIVO_CHOICES, null=True, blank=True)
    
    LUGAR_CHOICES = [
        ('casa', 'En Casa'),
        ('gimnasio', 'Gimnasio'),
        ('aire_libre', 'Al Aire Libre'),
    ]
    lugar_entrenamiento = models.CharField(max_length=20, choices=LUGAR_CHOICES, null=True, blank=True)

    # --- SEGURIDAD ---
    lesion_previa = models.BooleanField(default=False, verbose_name="¿Tienes alguna lesión diagnosticada?")
    descripcion_lesion = models.TextField(null=True, blank=True, verbose_name="Describe tu lesión")
    acepta_terminos = models.BooleanField(default=False, verbose_name="Acepto los términos y consentimiento informado")

    # --- SEGUIMIENTO Y CONTROL ---
    ultima_actividad = models.DateTimeField(auto_now=True) # Se actualiza solo
    
    ESTADO_CHOICES = [
        ('activo', 'Activo'),
        ('inactivo', 'Inactivo'),
        ('alerta', 'En Alerta'),
        ('pendiente', 'Pendiente de Revisión'),
    ]
    estado_cliente = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='activo')
    requiere_revision = models.BooleanField(default=False, verbose_name="Requiere Revisión Manual (EVA alto)")
    
    # --- MATCHMAKING ---
    coach_asignado = models.ForeignKey(
        'self', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        limit_choices_to={'es_coach': True}, # Solo permite elegir usuarios que sean coach
        related_name='mis_clientes'
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.username})"