"""authProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.shortcuts import redirect
from authApp import views
from authApp.admin import admin
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.urls import path

urlpatterns = [
    path('', TokenObtainPairView.as_view(), name='default-path'),
    # path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('admin/', admin.site.urls, name='admin'),
    path('login/', views.Login.as_view(), name='login'),
    path('refresh/', TokenRefreshView.as_view()),
    # path('logout/', views.Logout.as_view(), name='logout'),
    path('users/', views.UserView.as_view()),
    path('users/<int:pk>/', views.UserView.as_view()),
    path('users/username/<str:username>/', views.UserView.as_view()),
    path('roles/', views.RoleView.as_view()),
    path('roles/<int:pk>/', views.RoleView.as_view()),
    path('dependencias/', views.DependenciaView.as_view()),
    path('dependencias/<int:pk>/', views.DependenciaView.as_view()),
    path('series/', views.SerieView.as_view()),
    path('series/<int:pk>/', views.SerieView.as_view()),
    path('subseries/', views.SubSerieView.as_view()),
    path('subseries/<int:pk>/', views.SubSerieView.as_view()),
    path('contratos/', views.ContratoView.as_view()),
    path('contratos/<int:pk>/', views.ContratoView.as_view()),
    path('contratos/usuario/<int:usuario>/', views.ContratoView.as_view()),
    path('documentos/', views.DocumentoView.as_view()),
    path('documentos/<int:pk>/', views.DocumentoView.as_view()),
    path('documentos/contrato/<int:contrato>/', views.DocumentoView.as_view()),
    path('documentos/usuario/<int:usuario>/', views.DocumentoView.as_view()),
    path('historicos/', views.HistoricoView.as_view()),
    path('reportes/', views.ReporteView.as_view()),
    path('files/', views.SFTPFileList.as_view()),
    path('route/', views.ServidorView.as_view()),
    path('route/<int:pk>/', views.ServidorView.as_view()),

    path('<path:unknown_path>', lambda request, unknown_path: redirect('default-path')),
]
