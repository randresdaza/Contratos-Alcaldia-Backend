from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from authApp.models import Documento
from authApp.serializers.documentoSerializer import DocumentoSerializer
from authApp.signals import registrar_evento_documento_historico
from authApp.signals import registrar_evento_documento_reporte
from rest_framework.pagination import PageNumberPagination
from authApp.permissions import check_role


class DocumentoView(APIView):
    permission_classes = (IsAuthenticated,)
    pagination_class = PageNumberPagination

    @check_role(['Administrador', 'Supervisor', 'Digitador'])
    def get(self, request, pk=None, contrato=None, usuario=None):
        page_size = request.query_params.get('page_size', None)
        filter_name = request.query_params.get('filter', None)

        documents = Documento.objects.all().order_by('-id')

        if pk is not None:
            try:
                document = documents.get(id=pk)
                serializer = DocumentoSerializer(document)
                return Response(serializer.data)
            except Documento.DoesNotExist:
                return Response({'detail': 'El documento no existe'}, status=status.HTTP_404_NOT_FOUND)

        if contrato is not None:
            try:
                documents = documents.filter(contrato=contrato)
                if filter_name:
                    documents = documents.filter(nombre__icontains=filter_name)
                paginator = self.pagination_class()
                if page_size:
                    paginator.page_size = int(page_size)
                paginated_documents = paginator.paginate_queryset(documents, request)
                serializer = DocumentoSerializer(paginated_documents, many=True)
                return paginator.get_paginated_response(serializer.data)
            except Documento.DoesNotExist:
                return Response({'detail': 'El contrato no existe'}, status=status.HTTP_404_NOT_FOUND)

        if usuario is not None:
            try:
                documents = documents.filter(usuario=usuario)
                serializer = DocumentoSerializer(documents, many=True)
                return Response(serializer.data)
            except Documento.DoesNotExist:
                return Response({'detail': 'El usuario no existe'}, status=status.HTTP_404_NOT_FOUND)

        paginator = self.pagination_class()

        if page_size:
            paginator.page_size = int(page_size)
        paginated_documents = paginator.paginate_queryset(documents, request)
        serializer = DocumentoSerializer(paginated_documents, many=True)
        return paginator.get_paginated_response(serializer.data)

    @check_role(['Administrador', 'Supervisor', 'Digitador'])
    def post(self, request):
        serializer = DocumentoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            registrar_evento_documento_historico(sender=Documento, instance=serializer.instance, accion='GUARDADO',
                                                 user=request.user)
            registrar_evento_documento_reporte(instance=serializer.instance, user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @check_role(['Administrador', 'Supervisor', 'Digitador'])
    def put(self, request, pk):
        try:
            documento = Documento.objects.get(pk=pk)
        except Documento.DoesNotExist:
            return Response({'detail': 'El documento no existe'}, status=status.HTTP_404_NOT_FOUND)
        serializer = DocumentoSerializer(documento, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @check_role(['Administrador', 'Supervisor', 'Digitador'])
    def delete(self, request, pk):
        try:
            documento = Documento.objects.get(pk=pk)
        except Documento.DoesNotExist:
            return Response({'detail': 'El documento no existe'}, status=status.HTTP_404_NOT_FOUND)
        documento.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
