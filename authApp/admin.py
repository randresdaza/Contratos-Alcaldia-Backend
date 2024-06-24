from django.contrib import admin
from .models import User
from .models import Role
from .models import Contrato
from .models import Dependencia
from .models import Documento
from .models import Reporte
from .models import Serie
from .models import Subserie
from .models import Historico
from .models import Servidor

admin.site.site_header = 'Administración de Django - Contratos App'
# admin.site.site_title = 'Contratos'
admin.site.index_title = 'Bienvenido al sitio administrativo'


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'name', 'email', 'role', 'downloads', 'is_active', 'is_staff', 'is_superuser')
    list_filter = ('role', 'downloads', 'is_active', 'is_staff', 'is_superuser')
    search_fields = ('name', 'username', 'email')


class RoleAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


class DocumentoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'nro_paginas', 'contrato', 'fecha_creacion', 'usuario')
    list_filter = ('fecha_creacion',)
    search_fields = ('nombre',)


class ContratoAdmin(admin.ModelAdmin):
    list_display = ('asunto', 'fecha_inicial', 'fecha_final', 'estante', 'bandeja', 'caja', 'nro_orden', 'nro_folios',
                    'dependencia', 'serie', 'subserie', 'usuario')
    list_filter = ('fecha_inicial', 'fecha_final')
    search_fields = ('asunto',)


class DependenciaAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)


class ReporteAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'fecha', 'contrato', 'documento')
    list_filter = ('fecha',)
    search_fields = ('fecha',)


class SerieAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)


class SubserieAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)


class ServidorAdmin(admin.ModelAdmin):
    list_display = ('ruta',)
    search_fields = ('ruta',)


class HistoricoAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'fecha', 'accion', 'evento_sobre', 'contrato', 'documento')
    list_filter = ('fecha',)


admin.site.register(User, UserAdmin)
admin.site.register(Role, RoleAdmin)
admin.site.register(Documento, DocumentoAdmin)
admin.site.register(Contrato, ContratoAdmin)
admin.site.register(Dependencia, DependenciaAdmin)
admin.site.register(Reporte, ReporteAdmin)
admin.site.register(Serie, SerieAdmin)
admin.site.register(Subserie, SubserieAdmin)
admin.site.register(Historico, HistoricoAdmin)
admin.site.register(Servidor, ServidorAdmin)
