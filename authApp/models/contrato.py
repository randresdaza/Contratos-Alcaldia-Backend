from django.db import models
from .dependencia import Dependencia
from .serie import Serie
from .subserie import Subserie
from .user import User


class Contrato(models.Model):
    id = models.BigAutoField(primary_key=True)
    asunto = models.CharField('asunto', max_length=100, unique=True)
    fecha_inicial = models.DateField('fecha inicial')
    fecha_final = models.DateField('fecha final')
    estante = models.CharField('estante', max_length=10)
    bandeja = models.CharField('bandeja', max_length=10)
    caja = models.CharField('caja', max_length=10)
    nro_orden = models.CharField('n. orden', max_length=10)
    nro_folios = models.CharField('n. folios', max_length=10, default='0', null=True, blank=True)
    observaciones = models.CharField('observaciones', max_length=100, null=True, blank=True)
    dependencia = models.ForeignKey(Dependencia, on_delete=models.DO_NOTHING, verbose_name='dependencia')
    serie = models.ForeignKey(Serie, on_delete=models.DO_NOTHING, verbose_name='serie')
    subserie = models.ForeignKey(Subserie, on_delete=models.DO_NOTHING, verbose_name='subserie')
    usuario = models.ForeignKey(User, on_delete=models.DO_NOTHING, verbose_name='usuario')

    def __str__(self):
        return self.asunto
