from django.db import models
from django.contrib.auth.models import User

class PerfilUsuario(models.Model):
    """
    Modelo para estender o usuário padrão do Django com informações adicionais.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    biografia = models.TextField(verbose_name="Biografia", blank=True, null=True)
    data_nascimento = models.DateField(verbose_name="Data de Nascimento", blank=True, null=True)

    class Meta:
        verbose_name = "Perfil do Usuário"
        verbose_name_plural = "Perfis dos Usuários"

    def __str__(self):
        return self.user.username
