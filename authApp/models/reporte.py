from django.db import models
from .user import User
from .contrato import Contrato
from .documento import Documento


class Reporte(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    fecha = models.DateField(auto_now_add=True)
    contrato = models.ForeignKey(Contrato, on_delete=models.DO_NOTHING, null=True, verbose_name='asunto contrato')
    documento = models.ForeignKey(Documento, on_delete=models.DO_NOTHING, null=True, verbose_name='nombre documento' )
