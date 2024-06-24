from authApp.models.user import User
from authApp.models.role import Role
from rest_framework import serializers
from authApp.serializers.roleSerializer import RoleSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    pass


class CustomLoginUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'name', 'email', 'role', 'downloads')

    def to_representation(self, obj):
        role = obj.role
        role_serializer = RoleSerializer(role)
        return {
            'id': obj.id,
            'username': obj.username,
            'name': obj.name,
            'email': obj.email,
            'role': role_serializer.data,
            'downloads': obj.downloads
        }


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    role = serializers.PrimaryKeyRelatedField(queryset=Role.objects.all(), write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'name', 'email', 'role', 'is_active', 'password', 'downloads']

    def create(self, validated_data):
        role_id = validated_data.pop('role_id', None)
        user = User.objects.create(**validated_data)
        if role_id:
            user.role = role_id
            user.save()
        return user

    def to_representation(self, obj):
        role = obj.role
        role_serializer = RoleSerializer(role)
        return {
            'id': obj.id,
            'username': obj.username,
            'name': obj.name,
            'email': obj.email,
            'role': role_serializer.data,
            'is_active': obj.is_active,
            'downloads': obj.downloads
        }

    def update(self, instance, validated_data):
        if 'role_id' in validated_data:
            role_id = validated_data.pop('role_id')
            instance.role = role_id
        return super().update(instance, validated_data)
