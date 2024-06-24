from authApp.models.servidor import Servidor
from rest_framework import serializers


class ServidorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Servidor
        fields = ['id', 'ruta']
    
    def to_representation(self, obj):
        return {
            'id': obj.id,
            'ruta': obj.ruta,
        }
