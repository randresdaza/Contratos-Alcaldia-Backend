from authApp.models.documento import Documento
from authApp.models.user import User
from authApp.models.contrato import Contrato
from rest_framework import serializers
from authApp.serializers.contratoSerializer import ContratoSerializer
from authApp.serializers.userSerializer import UserSerializer


class DocumentoSerializer(serializers.ModelSerializer):
    usuario = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), write_only=True)
    contrato = serializers.PrimaryKeyRelatedField(queryset=Contrato.objects.all(), write_only=True)

    class Meta:
        model = Documento
        fields = ['id', 'nombre', 'fecha_creacion', 'nro_paginas', 'usuario', 'contrato']

    def create(self, validated_data):
        usuario_id = validated_data.pop('usuario_id', None)
        contrato_id = validated_data.pop('contrato_id', None)
        documento = Documento.objects.create(**validated_data)
        if usuario_id and contrato_id:
            documento.usuario = usuario_id
            documento.contrato = contrato_id
            documento.save()
        return documento

    def to_representation(self, obj):
        usuario = obj.usuario
        contrato = obj.contrato
        usuario_serializer = UserSerializer(usuario)
        contrato_serializer = ContratoSerializer(contrato)
        return {
            'id': obj.id,
            'nombre': obj.nombre,
            'fecha_creacion': obj.fecha_creacion,
            'nro_paginas': obj.nro_paginas,
            'usuario': usuario_serializer.data,
            'contrato': contrato_serializer.data,
        }

    def update(self, instance, validated_data):
        if 'usuario' in validated_data:
            usuario = validated_data.pop('usuario')
            instance.usuario = usuario
        if 'contrato' in validated_data:
            contrato = validated_data.pop('contrato')
            instance.contrato = contrato
        return super().update(instance, validated_data)
