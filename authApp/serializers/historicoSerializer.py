from authApp.models.historico import Historico
from authApp.models.user import User
from authApp.models.contrato import Contrato
from authApp.models.documento import Documento
from rest_framework import serializers
from authApp.serializers.userSerializer import UserSerializer
from authApp.serializers.contratoSerializer import ContratoSerializer
from authApp.serializers.documentoSerializer import DocumentoSerializer


class HistoricoSerializer(serializers.ModelSerializer):
    usuario = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), write_only=True)
    contrato = serializers.PrimaryKeyRelatedField(queryset=Contrato.objects.all(), write_only=True)
    documento = serializers.PrimaryKeyRelatedField(queryset=Documento.objects.all(), write_only=True)

    class Meta:
        model = Historico
        fields = ['id', 'evento_sobre', 'fecha', 'accion', 'usuario', 'contrato', 'documento']

    def create(self, validated_data):
        usuario_id = validated_data.pop('usuario_id', None)
        contrato_id = validated_data.pop('contrato_id', None)
        documento_id = validated_data.pop('documento_id', None)
        historico = Historico.objects.create(**validated_data)
        if usuario_id and contrato_id and documento_id:
            historico.usuario = usuario_id
            historico.contrato = contrato_id
            historico.documento = documento_id
            historico.save()
        return historico

    def to_representation(self, obj):
        usuario = obj.usuario
        contrato = obj.contrato
        documento = obj.documento
        user_serializer = UserSerializer(usuario)
        contrato_serializer = ContratoSerializer(contrato)
        documento_serializer = DocumentoSerializer(documento)
        return {
            'id': obj.id,
            'evento_sobre': obj.evento_sobre,
            'fecha': obj.fecha,
            'accion': obj.accion,
            'usuario': user_serializer.data,
            'contrato': contrato_serializer.data,
            'documento': documento_serializer.data,
        }

    def update(self, instance, validated_data):
        if 'usuario' in validated_data:
            usuario = validated_data.pop('usuario')
            instance.usuario = usuario
        if 'contrato' in validated_data:
            contrato = validated_data.pop('contrato')
            instance.contrato = contrato
        if 'documento' in validated_data:
            documento = validated_data.pop('documento')
            instance.documento = documento
        return super().update(instance, validated_data)
