from django.db import models


class Servidor(models.Model):
    id = models.BigAutoField(primary_key=True)
    ruta = models.TextField('ruta', unique=True)

    @classmethod
    def create_default_route(cls, route):
        if cls.objects.filter(ruta=route).exists():
            raise ValueError('La ruta ya existe.')
        servidor = cls(ruta=route)
        servidor.save()
        return servidor

    def __str__(self):
        return self.ruta
