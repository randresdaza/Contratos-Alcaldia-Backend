from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from authApp.models import Subserie
from authApp.serializers.subserieSerializer import SubserieSerializer
from rest_framework.pagination import PageNumberPagination
from authApp.permissions import check_role


class SubSerieView(APIView):
    permission_classes = (IsAuthenticated,)
    pagination_class = PageNumberPagination

    @check_role(['Administrador', 'Supervisor', 'Digitador'])
    def get(self, request, pk=None):
        page_size = request.query_params.get('page_size', None)
        filter_name = request.query_params.get('filter', None)

        subseries = Subserie.objects.all().order_by('-id')

        if pk is not None:
            try:
                subserie = Subserie.objects.get(pk=pk)
                serializer = SubserieSerializer(subserie)
                return Response(serializer.data)
            except Subserie.DoesNotExist:
                return Response({'detail': 'La subserie no existe'}, status=status.HTTP_404_NOT_FOUND)

        if filter_name:
            subseries = subseries.filter(nombre__icontains=filter_name)

        paginator = self.pagination_class()

        if page_size:
            paginator.page_size = int(page_size)

        paginated_subseries = paginator.paginate_queryset(subseries, request)
        serializer = SubserieSerializer(paginated_subseries, many=True)
        return paginator.get_paginated_response(serializer.data)

    @check_role(['Administrador', 'Supervisor', 'Digitador'])
    def post(self, request):
        serializer = SubserieSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @check_role(['Administrador', 'Supervisor', 'Digitador'])
    def put(self, request, pk):
        try:
            subserie = Subserie.objects.get(pk=pk)
        except Subserie.DoesNotExist:
            return Response({'detail': 'La subserie no existe'}, status=status.HTTP_404_NOT_FOUND)
        serializer = SubserieSerializer(subserie, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @check_role(['Administrador', 'Supervisor', 'Digitador'])
    def delete(self, request, pk):
        try:
            subserie = Subserie.objects.get(pk=pk)
        except Subserie.DoesNotExist:
            return Response({'detail': 'La subserie no existe'}, status=status.HTTP_404_NOT_FOUND)
        subserie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
