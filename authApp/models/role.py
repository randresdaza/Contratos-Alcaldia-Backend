from django.db import models


class Role (models.Model):
    id = models.BigAutoField(primary_key= True)
    name = models.CharField('nombre', max_length=50, unique=True)

    def __str__(self):
        return self.name
