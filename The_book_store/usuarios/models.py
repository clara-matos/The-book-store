from django.db import models
from django.contrib.auth.models import User

class Usuario(User):
    """
    Modelo para estender o usuário padrão do Django com informações adicionais.
    """
    biografia = models.TextField(verbose_name="Biografia", blank=True, null=True)
    data_nascimento = models.DateField(verbose_name="Data de Nascimento", blank=True, null=True)

    class Meta:
        verbose_name = "Perfil do Usuário"
        verbose_name_plural = "Perfis dos Usuários"

    def __str__(self):
        return self.user.username
