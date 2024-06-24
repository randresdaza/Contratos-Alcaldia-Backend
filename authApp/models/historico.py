from django.db import models
from .user import User
from .contrato import Contrato
from .documento import Documento


class Historico(models.Model):
    EVENTO_CHOICES = (
        ('contrato','Contrato'),
        ('documento', 'Documento'),
    )

    ACCION_CHOICES = (
        ('POST', 'GUARDADO'),
        ('PUT', 'EDITADO'),
        ('DELETE', 'ELIMINADO'),
    )

    contrato = models.ForeignKey(Contrato, on_delete=models.DO_NOTHING, null=True, verbose_name='asunto contrato')
    documento = models.ForeignKey(Documento, on_delete=models.DO_NOTHING, null=True, verbose_name='nombre documento')
    evento_sobre = models.CharField(max_length=20, choices=EVENTO_CHOICES)
    fecha = models.DateTimeField(auto_now_add=True)
    accion = models.CharField(choices=ACCION_CHOICES, max_length=10)
    usuario = models.ForeignKey(User, on_delete=models.DO_NOTHING)
