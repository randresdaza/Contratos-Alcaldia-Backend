from django.contrib.auth import authenticate
from django.contrib.sessions.models import Session
from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse
from django.utils import timezone
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from authApp.serializers.userSerializer import CustomTokenObtainPairSerializer, CustomLoginUserSerializer
from authApp.models.user import User
from authProject import settings


class Login(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        username = request.data.get('username', '')
        password = request.data.get('password', '')

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({'error': 'El usuario no se encuentra registrado.'}, status=status.HTTP_400_BAD_REQUEST)

        if user.is_active:
            user = authenticate(username=username, password=password)
            if user:
                login_serializer = self.serializer_class(data=request.data)
                if login_serializer.is_valid():
                    user_serializer = CustomLoginUserSerializer(user)
                    data = {
                        'access': login_serializer.validated_data.get('access'),
                        'refresh': login_serializer.validated_data.get('refresh'),
                        'user': user_serializer.data,
                        'message': 'Inicio de sesión exitoso.'
                    }
                    response = JsonResponse(data, status=status.HTTP_200_OK, encoder=DjangoJSONEncoder)
                    response.set_cookie('token_cookie_access', data['access'], httponly=True,
                                        max_age=int(settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'].total_seconds()),
                                        secure=True, samesite='Strict')
                    response.set_cookie('token_cookie_refresh', data['refresh'], httponly=True,
                                        max_age=int(settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'].total_seconds()),
                                        secure=True, samesite='Strict')
                    return response
            else:
                return Response({'error': 'Contraseña incorrecta.'},
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'Este usuario no puede iniciar sesión.'}, status=status.HTTP_400_BAD_REQUEST)


class Logout(GenericAPIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username', '')
        user = User.objects.filter(username=username).first()
        if user:
            refresh = request.data.get('refresh', '')
            if not refresh:
                return Response({'error': 'Refresh token no proporcionado.'}, status=status.HTTP_400_BAD_REQUEST)
            try:
                sessions = Session.objects.filter(expire_date__gte=timezone.now())
                for session in sessions:
                    data = session.get_decoded()
                    if data.get('_auth_user_id') == str(user.id):
                        session.delete()
                return Response({'message': 'Sesión cerrada correctamente.'}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error': 'No existe este usuario.'}, status=status.HTTP_400_BAD_REQUEST)
