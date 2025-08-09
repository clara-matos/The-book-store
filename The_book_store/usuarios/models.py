from django.db import models
from django.contrib.auth.models import User

class PerfilUsuario(models.Model):
    """
    Modelo para estender o usuário padrão do Django com informações adicionais.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    
    class Meta:
        verbose_name = "Perfil do Usuário"
        verbose_name_plural = "Perfis dos Usuários"

    def __str__(self):
        return self.user.username
