from authApp.models.reporte import Reporte
from authApp.models.user import User
from authApp.models.contrato import Contrato
from authApp.models.documento import Documento
from rest_framework import serializers
from authApp.serializers.userSerializer import UserSerializer
from authApp.serializers.contratoSerializer import ContratoSerializer
from authApp.serializers.documentoSerializer import DocumentoSerializer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'name', 'email')


class ReporteSerializer(serializers.ModelSerializer):
    usuario = UserSerializer()
    contrato = serializers.PrimaryKeyRelatedField(queryset=Contrato.objects.all(), write_only=True)
    documento = serializers.PrimaryKeyRelatedField(queryset=Documento.objects.all(), write_only=True)

    class Meta:
        model = Reporte
        fields = ['id', 'usuario', 'fecha', 'contrato', 'documento']

    def create(self, validated_data):
        usuario_data = validated_data.pop('usuario', None)
        contrato = validated_data.pop('contrato', None)
        documento = validated_data.pop('documento', None)
        reporte = Reporte.objects.create(**validated_data)
        if usuario_data:
            usuario, created = User.objects.get_or_create(**usuario_data)
        if contrato:
            reporte.contrato = contrato
        if documento:
            reporte.documento = documento
        reporte = Reporte.objects.create(usuario=usuario, contrato=contrato, documento=documento, **validated_data)
        return reporte

    def to_representation(self, obj):
        usuario = obj.usuario
        contrato = obj.contrato
        documento = obj.documento
        user_serializer = UserSerializer(usuario)
        contrato_serializer = ContratoSerializer(contrato)
        documento_serializer = DocumentoSerializer(documento)
        return {
            'id': obj.id,
            'usuario': user_serializer.data,
            'fecha': obj.fecha,
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
