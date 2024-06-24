from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from authApp.models import Role
from authApp.serializers.roleSerializer import RoleSerializer
from authApp.permissions import check_role


class RoleView(APIView):
    permission_classes = (IsAuthenticated,)

    @check_role(['Administrador'])
    def get(self, request, pk=None):
        if pk is not None:
            try:
                role = Role.objects.get(pk=pk)
                serializer = RoleSerializer(role)
                return Response(serializer.data)
            except Role.DoesNotExist:
                return Response({'detail': 'El rol no existe'}, status=status.HTTP_404_NOT_FOUND)
        roles = Role.objects.all().order_by('id')
        serializer = RoleSerializer(roles, many=True)
        return Response(serializer.data)

    @check_role(['Administrador'])
    def post(self, request):
        serializer = RoleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @check_role(['Administrador'])
    def put(self, request, pk):
        try:
            role = Role.objects.get(pk=pk)
        except Role.DoesNotExist:
            return Response({'detail': 'El rol no existe'}, status=status.HTTP_404_NOT_FOUND)
        serializer = RoleSerializer(role, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @check_role(['Administrador'])
    def delete(self, request, pk):
        try:
            role = Role.objects.get(pk=pk)
        except Role.DoesNotExist:
            return Response({'detail': 'El rol no existe'}, status=status.HTTP_404_NOT_FOUND)
        role.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
