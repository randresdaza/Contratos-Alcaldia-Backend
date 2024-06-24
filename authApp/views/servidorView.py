from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from authApp.models import Servidor
from authApp.serializers.servidorSerializer import ServidorSerializer
from authApp.permissions import check_role


class ServidorView(APIView):
    permission_classes = (IsAuthenticated,)

    @check_role(['Administrador'])
    def get(self, request, pk=None):
        if pk is not None:
            try:
                route = Servidor.objects.get(pk=pk)
                serializer = ServidorSerializer(route)
                return Response(serializer.data)
            except Servidor.DoesNotExist:
                return Response({'detail': 'La ruta no existe'}, status=status.HTTP_404_NOT_FOUND)
        routes = Servidor.objects.all()
        serializer = ServidorSerializer(routes, many=True)
        return Response(serializer.data)

    # def post(self, request):
    #     serializer = ServidorSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @check_role(['Administrador'])
    def put(self, request, pk):
        try:
            ruta = Servidor.objects.get(pk=pk)
        except Servidor.DoesNotExist:
            return Response({'detail': 'La ruta no existe'}, status=status.HTTP_404_NOT_FOUND)
        serializer = ServidorSerializer(ruta, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
