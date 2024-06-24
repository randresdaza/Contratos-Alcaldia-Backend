from authApp.models.subserie import Subserie
from rest_framework import serializers


class SubserieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subserie
        fields = ['id', 'nombre']
    
    def to_representation(self, obj):
        return {
            'id': obj.id,
            'nombre': obj.nombre,
        }
