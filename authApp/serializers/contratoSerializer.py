from authApp.models.contrato import Contrato
from authApp.models.dependencia import Dependencia
from authApp.models.serie import Serie
from authApp.models.user import User
from authApp.models.subserie import Subserie
from rest_framework import serializers
from authApp.serializers.dependenciaSerializer import DependenciaSerializer
from authApp.serializers.serieSerializer import SerieSerializer
from authApp.serializers.subserieSerializer import SubserieSerializer
from authApp.serializers.userSerializer import UserSerializer


class ContratoSerializer(serializers.ModelSerializer):
    dependencia = serializers.PrimaryKeyRelatedField(queryset=Dependencia.objects.all(), write_only=True)
    serie = serializers.PrimaryKeyRelatedField(queryset=Serie.objects.all(), write_only=True)
    subserie = serializers.PrimaryKeyRelatedField(queryset=Subserie.objects.all(), write_only=True)
    usuario = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), write_only=True)

    # fecha_inicial = serializers.DateField(format="%d-%m-%Y")
    # fecha_final = serializers.DateField(format="%d-%m-%Y")

    class Meta:
        model = Contrato
        fields = ['id', 'asunto', 'fecha_inicial', 'fecha_final', 'estante', 'bandeja', 'caja', 'nro_orden',
                  'nro_folios', 'observaciones', 'dependencia', 'serie', 'subserie', 'usuario']

    def create(self, validated_data):
        dependencia_id = validated_data.pop('dependencia_id', None)
        serie_id = validated_data.pop('serie_id', None)
        subserie_id = validated_data.pop('subserie_id', None)
        usuario_id = validated_data.pop('usuario_id', None)
        contrato = Contrato.objects.create(**validated_data)
        if dependencia_id and serie_id and subserie_id and usuario_id:
            contrato.dependencia = dependencia_id
            contrato.serie = serie_id
            contrato.subserie = subserie_id
            contrato.usuario = usuario_id
            contrato.save()
        return contrato

    def to_representation(self, obj):
        dependencia = obj.dependencia
        serie = obj.serie
        subserie = obj.subserie
        usuario = obj.usuario
        dependencia_serializer = DependenciaSerializer(dependencia)
        serie_serializer = SerieSerializer(serie)
        subserie_serializer = SubserieSerializer(subserie)
        user_serializer = UserSerializer(usuario)
        return {
            'id': obj.id,
            'asunto': obj.asunto,
            'fecha_inicial': obj.fecha_inicial,
            'fecha_final': obj.fecha_final,
            'estante': obj.estante,
            'bandeja': obj.bandeja,
            'caja': obj.caja,
            'nro_orden': obj.nro_orden,
            'nro_folios': obj.nro_folios,
            'observaciones': obj.observaciones,
            'dependencia': dependencia_serializer.data,
            'serie': serie_serializer.data,
            'subserie': subserie_serializer.data,
            'usuario': user_serializer.data,
        }

    def update(self, instance, validated_data):
        if 'dependencia' in validated_data:
            dependencia = validated_data.pop('dependencia')
            instance.dependencia = dependencia
        if 'serie' in validated_data:
            serie = validated_data.pop('serie')
            instance.serie = serie
        if 'subserie' in validated_data:
            subserie = validated_data.pop('subserie')
            instance.subserie = subserie
        if 'usuario' in validated_data:
            usuario = validated_data.pop('usuario')
            instance.usuario = usuario
        return super().update(instance, validated_data)
