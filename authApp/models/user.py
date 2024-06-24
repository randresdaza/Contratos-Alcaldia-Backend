from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.contrib.auth.hashers import make_password
from .role import Role


class UserManager(BaseUserManager):
    def create_user(self, username, password):
        if not username:
            raise ValueError('El nombre de usuario ya existe')
        user = self.model(username=username, password=password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, password):
        user = self.create_user(username=username, password=password)
        user.is_superuser = True
        user.is_staff = True
        rol_administrador, creado = Role.objects.get_or_create(name='Administrador')
        user.role = rol_administrador
        user.name = 'Administrador'
        user.email = 'admin@admin.com'
        user.is_active = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    id = models.BigAutoField(primary_key=True)
    username = models.CharField('usuario', max_length=30, unique=True)
    password = models.CharField('contraseña', max_length=256, blank=True)
    name = models.CharField('nombre', max_length=100)
    email = models.EmailField('correo', max_length=256, unique=True)
    role = models.ForeignKey(Role, on_delete=models.DO_NOTHING, verbose_name='rol')
    downloads = models.BooleanField(
        'descargas',
        default=False,
        help_text='Indica si el usuario puede descargar archivos.'
    )
    is_active = models.BooleanField(
        'estado',
        default=False,
        help_text='Indica si el usuario puede iniciar sesión.'
    )
    is_staff = models.BooleanField(
        'es personal admin.',
        default=False,
        help_text='Indica que este usuario es personal administrativo y puede ingresar al panel.'
    )

    def save(self, *args, **kwargs):
        if not self.pk:
            self.password = make_password(self.password)
        else:
            user = User.objects.get(pk=self.pk)
            if self.password != user.password:
                self.password = make_password(self.password)

        if self.role_id is None:
            role, created = Role.objects.get_or_create(name='Administrador')
            self.role = role

        if self.role.name == 'Administrador':
            self.downloads = True
        super().save(*args, **kwargs)
    
    objects = UserManager()
    USERNAME_FIELD = 'username'
