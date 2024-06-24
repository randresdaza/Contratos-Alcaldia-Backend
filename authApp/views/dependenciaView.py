from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from authApp.models import Dependencia
from authApp.serializers.dependenciaSerializer import DependenciaSerializer
from rest_framework.pagination import PageNumberPagination
from authApp.permissions import check_role


class DependenciaView(APIView):
    permission_classes = (IsAuthenticated,)
    pagination_class = PageNumberPagination

    @check_role(['Administrador', 'Supervisor', 'Digitador'])
    def get(self, request, pk=None):
        page_size = request.query_params.get('page_size', None)
        filter_name = request.query_params.get('filter', None)

        dependencias = Dependencia.objects.all().order_by('-id')

        if pk is not None:
            try:
                dependencia = Dependencia.objects.get(pk=pk)
                serializer = DependenciaSerializer(dependencia)
                return Response(serializer.data)
            except Dependencia.DoesNotExist:
                return Response({'detail': 'La dependencia no existe'}, status=status.HTTP_404_NOT_FOUND)

        if filter_name:
            dependencias = dependencias.filter(nombre__icontains=filter_name)

        paginator = self.pagination_class()

        if page_size:
            paginator.page_size = int(page_size)

        paginated_dependencies = paginator.paginate_queryset(dependencias, request)
        serializer = DependenciaSerializer(paginated_dependencies, many=True)
        return paginator.get_paginated_response(serializer.data)

    @check_role(['Administrador', 'Supervisor', 'Digitador'])
    def post(self, request):
        serializer = DependenciaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @check_role(['Administrador', 'Supervisor', 'Digitador'])
    def put(self, request, pk):
        try:
            dependencia = Dependencia.objects.get(pk=pk)
        except Dependencia.DoesNotExist:
            return Response({'detail': 'La dependencia no existe'}, status=status.HTTP_404_NOT_FOUND)
        serializer = DependenciaSerializer(dependencia, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @check_role(['Administrador', 'Supervisor', 'Digitador'])
    def delete(self, request, pk):
        try:
            dependencia = Dependencia.objects.get(pk=pk)
        except Dependencia.DoesNotExist:
            return Response({'detail': 'La dependencia no existe'}, status=status.HTTP_404_NOT_FOUND)
        dependencia.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
