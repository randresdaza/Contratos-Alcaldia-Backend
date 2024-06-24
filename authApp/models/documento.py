from django.db import models
from .user import User
from .contrato import Contrato


class Documento(models.Model):
    id = models.BigAutoField(primary_key=True)
    nombre = models.CharField(max_length=200, unique=True, null=True, blank=True)
    fecha_creacion = models.DateTimeField('fecha creación' ,null=True, blank=True)
    nro_paginas = models.CharField('n. paginas',max_length=10, null=True, blank=True)
    usuario = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    contrato = models.ForeignKey(Contrato, on_delete=models.DO_NOTHING, verbose_name='asunto contrato')

    def __str__(self):
        return self.nombre
