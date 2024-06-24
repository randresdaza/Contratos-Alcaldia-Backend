from authApp.models.role import Role
from rest_framework import serializers


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['id', 'name']
    
    def to_representation(self, obj):
        return {
            'id': obj.id,
            'name': obj.name,
        }
