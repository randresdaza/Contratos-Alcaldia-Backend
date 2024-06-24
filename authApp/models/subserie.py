from django.db import models


class Subserie (models.Model):
    id = models.BigAutoField(primary_key=True)
    nombre = models.CharField('nombre', max_length=50, unique=True)

    def __str__(self):
        return self.nombre
