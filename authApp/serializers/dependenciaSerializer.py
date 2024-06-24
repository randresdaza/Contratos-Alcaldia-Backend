from authApp.models.dependencia import Dependencia
from rest_framework import serializers


class DependenciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dependencia
        fields = ['id', 'nombre']
    
    def to_representation(self, obj):
        return {
            'id': obj.id,
            'nombre': obj.nombre,
        }
