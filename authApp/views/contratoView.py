from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from authApp.models import Contrato
from authApp.serializers.contratoSerializer import ContratoSerializer
from authApp.signals import registrar_evento_contrato_historico
from authApp.signals import registrar_evento_contrato_reporte
from rest_framework.pagination import PageNumberPagination
from datetime import datetime
from authApp.permissions import check_role


class ContratoView(APIView):
    permission_classes = (IsAuthenticated,)
    pagination_class = PageNumberPagination

    @check_role(['Administrador', 'Supervisor', 'Digitador'])
    def get(self, request, pk=None, usuario=None):
        page_size = request.query_params.get('page_size', None)
        filter_asunto = request.query_params.get('filter', None)
        init_date = request.query_params.get('initDate')
        end_date = request.query_params.get('endDate')

        init_date = datetime.strptime(init_date, '%Y-%m-%d') if init_date else None
        end_date = datetime.strptime(end_date, '%Y-%m-%d') if end_date else None

        contratos = Contrato.objects.all().order_by('-id')

        if pk is not None:
            try:
                contrato = Contrato.objects.get(id=pk)
                serializer = ContratoSerializer(contrato)
                return Response(serializer.data)
            except Contrato.DoesNotExist:
                return Response({'detail': 'El contrato no existe'}, status=status.HTTP_404_NOT_FOUND)

        if init_date and end_date:
            contratos = contratos.filter(fecha_inicial__gte=init_date, fecha_final__lte=end_date)
        elif init_date:
            contratos = contratos.filter(fecha_inicial=init_date)
        elif end_date:
            contratos = contratos.filter(fecha_final=end_date)

        if filter_asunto:
            contratos = contratos.filter(asunto__icontains=filter_asunto)

        paginator = self.pagination_class()

        if page_size:
            paginator.page_size = int(page_size)

        paginated_contracts = paginator.paginate_queryset(contratos, request)
        serializer = ContratoSerializer(paginated_contracts, many=True)
        return paginator.get_paginated_response(serializer.data)

    @check_role(['Administrador', 'Supervisor', 'Digitador'])
    def post(self, request):
        serializer = ContratoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            registrar_evento_contrato_historico(sender=Contrato, instance=serializer.instance, accion='GUARDADO',
                                                user=request.user)
            registrar_evento_contrato_reporte(instance=serializer.instance, user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @check_role(['Administrador', 'Supervisor', 'Digitador'])
    def put(self, request, pk):
        try:
            contrato = Contrato.objects.get(pk=pk)
        except Contrato.DoesNotExist:
            return Response({'detail': 'El contrato no existe'}, status=status.HTTP_404_NOT_FOUND)
        serializer = ContratoSerializer(contrato, data=request.data)
        if serializer.is_valid():
            serializer.save()
            registrar_evento_contrato_historico(sender=Contrato, instance=serializer.instance, accion='EDITADO',
                                                user=request.user)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @check_role(['Administrador', 'Supervisor', 'Digitador'])
    def delete(self, request, pk):
        try:
            contrato = Contrato.objects.get(pk=pk)
        except Contrato.DoesNotExist:
            return Response({'detail': 'El contrato no existe'}, status=status.HTTP_404_NOT_FOUND)
        contrato.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
