from authApp.models.serie import Serie
from rest_framework import serializers


class SerieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Serie
        fields = ['id', 'nombre']
    
    def to_representation(self, obj):
        return {
            'id': obj.id,
            'nombre': obj.nombre,
        }
