from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models


class Alerta(models.Model):
    maquina = models.CharField(max_length=100)
    descripcion = models.TextField()
    usuario = models.ForeignKey(User, on_delete=models.PROTECT)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Alerta {self.id} - {self.maquina}'


class Parada(models.Model):
    maquina = models.CharField(max_length=100)
    inicio = models.DateTimeField()
    fin = models.DateTimeField()
    motivo = models.TextField()
    usuario = models.ForeignKey(User, on_delete=models.PROTECT)

    # Datos de cancelación (vacíos mientras la parada no esté cancelada)
    cancelada_por = models.ForeignKey(
        User, on_delete=models.PROTECT, null=True, blank=True, related_name='paradas_canceladas'
    )
    cancelada_en = models.DateTimeField(null=True, blank=True)
    motivo_cancelacion = models.TextField(blank=True)

    def clean(self):
        # La parada debe terminar después de empezar
        if self.inicio and self.fin and self.fin <= self.inicio:
            raise ValidationError('La finalización debe ser posterior al inicio.')

    def duracion_minutos(self):
        segundos = (self.fin - self.inicio).total_seconds()
        return int(segundos // 60)

    def __str__(self):
        return f'Parada {self.id} - {self.maquina}'
