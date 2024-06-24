from django.db.models.signals import post_save, post_migrate
from django.dispatch import receiver
from authApp.models import User, Contrato, Documento, Historico, Reporte, Servidor


@receiver(post_migrate)
def create_default_admin_user(sender, **kwargs):
    if sender.name == 'authApp':
        if not User.objects.filter(username='admin').exists():
            admin_user = User.objects.create_superuser('admin', 'admin')
            admin_user.save()


@receiver(post_migrate)
def create_default_ruta_servidor(sender, **kwargs):
    if sender.name == 'authApp':
        if not Servidor.objects.exists():
            route_server = Servidor.create_default_route('/home/rafael_upc/contratos/files')
            route_server.save()


@receiver(post_save, sender=Contrato)
def registrar_evento_contrato_historico(sender, instance, **kwargs):
    contrato_id = instance.id
    evento_sobre = sender.__name__.lower()
    user = kwargs.get('user', None)
    accion = kwargs.get('accion', None)
    if user:
        user_id = user.id
        Historico.objects.create(contrato_id=contrato_id, evento_sobre=evento_sobre, accion=accion, usuario_id=user_id)


@receiver(post_save, sender=Documento)
def registrar_evento_documento_historico(sender, instance, **kwargs):
    documento_id = instance.id
    evento_sobre = sender.__name__.lower()
    user = kwargs.get('user', None)
    accion = kwargs.get('accion', None)
    if user:
        user_id = user.id
        Historico.objects.create(documento_id=documento_id, evento_sobre=evento_sobre, accion=accion,
                                 usuario_id=user_id)


@receiver(post_save, sender=Reporte)
def registrar_evento_contrato_reporte(instance, **kwargs):
    contrato_id = instance.id
    user = kwargs.get('user', None)
    if user:
        user_id = user.id
        Reporte.objects.create(usuario_id=user_id, contrato_id=contrato_id)


@receiver(post_save, sender=Reporte)
def registrar_evento_documento_reporte(instance, **kwargs):
    documento_id = instance.id
    user = kwargs.get('user', None)
    if user:
        user_id = user.id
        Reporte.objects.create(usuario_id=user_id, documento_id=documento_id)
