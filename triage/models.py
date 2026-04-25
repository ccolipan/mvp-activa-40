from django.db import models
from django.conf import settings

class Restriccion_Fisica(models.Model):
    # Ej: "Lesión Lumbar", "Dolor de Rodilla", "Hipertensión"
    nombre = models.CharField(max_length=100, verbose_name="Zona de dolor o Patología")
    descripcion = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Restricción Física"
        verbose_name_plural = "Restricciones Físicas"

    def __str__(self):
        return self.nombre

class Ejercicio(models.Model):
    nombre = models.CharField(max_length=100, verbose_name="Nombre del Ejercicio")
    grupo_muscular = models.CharField(max_length=100, verbose_name="Grupo Muscular")
    
    # RELACIÓN MUCHOS A MUCHOS: Aquí conectamos el ejercicio con las restricciones 
    # a través de la clase intermedia "Contraindicacion".
    restricciones_vinculadas = models.ManyToManyField(
        Restriccion_Fisica, 
        through='Contraindicacion',
        verbose_name="Contraindicado para"
    )

    class Meta:
        verbose_name = "Ejercicio"
        verbose_name_plural = "Ejercicios"

    def __str__(self):
        return self.nombre

class Contraindicacion(models.Model):
    # Clase intermedia: Define EXACTAMENTE por qué un ejercicio está bloqueado.
    ejercicio = models.ForeignKey(Ejercicio, on_delete=models.CASCADE)
    restriccion = models.ForeignKey(Restriccion_Fisica, on_delete=models.CASCADE)
    
    # Podría ser un bloqueo total o solo una advertencia
    es_bloqueo_absoluto = models.BooleanField(
        default=True, 
        verbose_name="¿Bloquea el ejercicio por completo?"
    )

    class Meta:
        verbose_name = "Contraindicación"
        verbose_name_plural = "Contraindicaciones"

    def __str__(self):
        return f"Bloqueo: {self.ejercicio.nombre} por {self.restriccion.nombre}"

class Usuario_Restriccion(models.Model):
    # Aquí registramos lo que el usuario declara en su "Triage" inicial.
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    restriccion = models.ForeignKey(Restriccion_Fisica, on_delete=models.CASCADE)
    
    # Escala clínica de dolor (1 al 10)
    nivel_dolor_eva = models.IntegerField(
        choices=[(i, str(i)) for i in range(1, 11)],
        verbose_name="Nivel de Dolor (EVA 1-10)"
    )
    fecha_registro = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Restricción de Usuario"
        verbose_name_plural = "Restricciones de Usuarios"

    def __str__(self):
        return f"{self.usuario.first_name} sufre de {self.restriccion.nombre} (EVA: {self.nivel_dolor_eva})"