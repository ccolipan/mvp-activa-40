from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from triage.models import Ejercicio, Usuario_Restriccion, Contraindicacion

class Rutina(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='rutinas_cliente')
    coach = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='rutinas_coach')
    fecha_asignacion = models.DateField(auto_now_add=True)
    completada = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Rutina"
        verbose_name_plural = "Rutinas"

    def __str__(self):
        return f"Rutina de {self.usuario.first_name} - {self.fecha_asignacion}"

class Detalle_Rutina(models.Model):
    rutina = models.ForeignKey(Rutina, on_delete=models.CASCADE, related_name='detalles')
    ejercicio = models.ForeignKey(Ejercicio, on_delete=models.CASCADE)
    series = models.IntegerField(default=3)
    repeticiones = models.IntegerField(default=10)
    peso_sugerido_kg = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    class Meta:
        verbose_name = "Detalle de Rutina"
        verbose_name_plural = "Detalles de Rutina"

    def clean(self):
        super().clean()
        
        usuario_actual = self.rutina.usuario
        dolores_riesgo = Usuario_Restriccion.objects.filter(usuario=usuario_actual, nivel_dolor_eva__gte=4)

        for dolor in dolores_riesgo:
            bloqueo_activo = Contraindicacion.objects.filter(
                ejercicio=self.ejercicio,
                restriccion=dolor.restriccion,
                es_bloqueo_absoluto=True
            ).exists()

            if bloqueo_activo:
                raise ValidationError(
                    f"🛑 BLOQUEO DE TRIAGE: No puedes asignar '{self.ejercicio.nombre}'. "
                    f"El cliente presenta dolor en: {dolor.restriccion.nombre} (EVA: {dolor.nivel_dolor_eva}/10)."
                )

    def __str__(self):
        return f"{self.ejercicio.nombre} ({self.series}x{self.repeticiones})"

class Evaluacion_PostSesion(models.Model):
    rutina = models.OneToOneField(Rutina, on_delete=models.CASCADE)
    esfuerzo_rpe = models.IntegerField(choices=[(i, str(i)) for i in range(1, 11)], verbose_name="Esfuerzo Percibido (RPE 1-10)")
    comentario_usuario = models.TextField(blank=True, null=True)
    fecha_evaluacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Evaluación Post-Sesión"
        verbose_name_plural = "Evaluaciones Post-Sesión"

    def __str__(self):
        return f"RPE: {self.esfuerzo_rpe} - {self.rutina.usuario.first_name}"

class Alerta_Inactividad(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    dias_inactividad = models.IntegerField(choices=[(3, '3 Días'), (7, '7 Días'), (14, '14 Días')])
    fecha_disparo = models.DateTimeField(auto_now_add=True)
    resuelta = models.BooleanField(default=False, verbose_name="¿Contactado por Coach?")

    class Meta:
        verbose_name = "Alerta de Inactividad"
        verbose_name_plural = "Alertas de Inactividad"

    def __str__(self):
        return f"ALERTA {self.dias_inactividad} días: {self.usuario.first_name}"