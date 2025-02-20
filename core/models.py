from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
import os

# função para definir o nome da foto de perfil
def foto_perfil_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f'{instance.username}.{ext}'
    return os.path.join('fotos_perfil', filename)

class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError("Usuário devem ter um nome.")
        
        user = self.model(username=username, **extra_fields)

        # senha
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, password, **extra_fields)

class CustomUser(AbstractUser):
    class VinculoChoices(models.TextChoices):
        BOLSISTA = 'bolsista', 'Bolsista'
        PROFESSOR = 'professor', 'Professor'
        COORDENADOR = 'coordenador', 'Coordenador'
    
    vinculo = models.CharField(max_length=100, choices=VinculoChoices.choices)
    matricula = models.CharField(max_length=100, null=True, blank=True, unique=True)
    foto_perfil = models.ImageField(upload_to=foto_perfil_path, default='fotos_perfil/default.png', 
                                    null=True, blank=True, verbose_name='Foto de Perfil')

    objects = CustomUserManager()

    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
    
    # sobreescrevendo o método save para deletar a foto de perfil antiga quando o usuário é atualizado
    def save(self, *args, **kwargs):
        if self.pk:
            try:
                old_instance = CustomUser.objects.get(pk=self.pk)
                if old_instance.foto_perfil and old_instance.foto_perfil != 'fotos_perfil/default.png':
                    if self.foto_perfil != old_instance.foto_perfil:
                        old_instance.foto_perfil.delete(save=False)
            except CustomUser.DoesNotExist:
                pass
        super().save(*args, **kwargs)
