from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from authApp.models import User
from authApp.serializers.userSerializer import UserSerializer
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from authApp.permissions import check_role


class UserView(APIView):
    permission_classes = (IsAuthenticated,)
    pagination_class = PageNumberPagination

    @check_role(['Administrador'])
    def get(self, request, pk=None, username=None):
        page_size = request.query_params.get('page_size', None)
        filter_user = request.query_params.get('filter', None)

        users = User.objects.all().order_by('-id')

        if pk is not None:
            try:
                user = User.objects.get(id=pk)
                serializer = UserSerializer(user)
                return Response(serializer.data)
            except User.DoesNotExist:
                return Response({'detail': 'El usuario no existe'}, status=status.HTTP_404_NOT_FOUND)

        if username is not None:
            try:
                user = User.objects.get(username=username)
                serializer = UserSerializer(user)
                return Response(serializer.data)
            except User.DoesNotExist:
                return Response({'detail': 'El usuario no existe'}, status=status.HTTP_404_NOT_FOUND)

        if filter_user:
            users = users.filter(
                Q(username__icontains=filter_user) |
                Q(name__icontains=filter_user) |
                Q(email__icontains=filter_user) |
                Q(role__name__icontains=filter_user)
            )

        paginator = self.pagination_class()

        if page_size:
            paginator.page_size = int(page_size)

        paginated_users = paginator.paginate_queryset(users, request)
        serializer = UserSerializer(paginated_users, many=True)
        return paginator.get_paginated_response(serializer.data)

    @check_role(['Administrador'])
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @check_role(['Administrador'])
    def put(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({'detail': 'El usuario no existe'}, status=status.HTTP_404_NOT_FOUND)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @check_role(['Administrador'])
    def delete(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({'detail': 'El usuario no existe'}, status=status.HTTP_404_NOT_FOUND)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
