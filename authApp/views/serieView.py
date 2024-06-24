from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from authApp.models import Serie
from authApp.serializers.serieSerializer import SerieSerializer
from rest_framework.pagination import PageNumberPagination
from authApp.permissions import check_role


class SerieView(APIView):
    permission_classes = (IsAuthenticated,)
    pagination_class = PageNumberPagination

    @check_role(['Administrador', 'Supervisor', 'Digitador'])
    def get(self, request, pk=None):
        page_size = request.query_params.get('page_size', None)
        filter_name = request.query_params.get('filter', None)

        series = Serie.objects.all().order_by('-id')

        if pk is not None:
            try:
                serie = Serie.objects.get(pk=pk)
                serializer = SerieSerializer(serie)
                return Response(serializer.data)
            except Serie.DoesNotExist:
                return Response({'detail': 'La serie no existe'}, status=status.HTTP_404_NOT_FOUND)

        if filter_name:
            series = series.filter(nombre__icontains=filter_name)

        paginator = self.pagination_class()

        if page_size:
            paginator.page_size = int(page_size)

        paginated_series = paginator.paginate_queryset(series, request)
        serializer = SerieSerializer(paginated_series, many=True)
        return paginator.get_paginated_response(serializer.data)

    @check_role(['Administrador', 'Supervisor', 'Digitador'])
    def post(self, request):
        serializer = SerieSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @check_role(['Administrador', 'Supervisor', 'Digitador'])
    def put(self, request, pk):
        try:
            serie = Serie.objects.get(pk=pk)
        except Serie.DoesNotExist:
            return Response({'detail': 'La serie no existe'}, status=status.HTTP_404_NOT_FOUND)
        serializer = SerieSerializer(serie, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @check_role(['Administrador', 'Supervisor', 'Digitador'])
    def delete(self, request, pk):
        try:
            serie = Serie.objects.get(pk=pk)
        except Serie.DoesNotExist:
            return Response({'detail': 'La serie no existe'}, status=status.HTTP_404_NOT_FOUND)
        serie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
