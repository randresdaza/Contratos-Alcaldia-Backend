from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from authApp.models import Historico
from authApp.serializers.historicoSerializer import HistoricoSerializer
from datetime import datetime
from authApp.permissions import check_role


class HistoricoView(APIView):
    permission_classes = (IsAuthenticated,)
    pagination_class = PageNumberPagination

    @check_role(['Administrador', 'Supervisor'])
    def get(self, request):
        page_size = request.query_params.get('page_size', None)
        filter_username = request.query_params.get('filter', None)
        from_date = request.query_params.get('fromDate')
        to_date = request.query_params.get('toDate')

        from_date = datetime.strptime(from_date, '%Y-%m-%d') if from_date else None
        to_date = datetime.strptime(to_date, '%Y-%m-%d') if to_date else None

        historicos = Historico.objects.all().order_by('-id')

        if from_date and to_date:
            historicos = historicos.filter(fecha__date__range=(from_date.date(), to_date.date()))

        if filter_username:
            historicos = historicos.filter(usuario__username__icontains=filter_username)

        paginator = self.pagination_class()

        if page_size:
            paginator.page_size = int(page_size)

        paginated_historicos = paginator.paginate_queryset(historicos, request)

        serializer = HistoricoSerializer(paginated_historicos, many=True)

        return paginator.get_paginated_response(serializer.data)
