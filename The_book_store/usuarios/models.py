from django.db import models
from django.contrib.auth.models import User, Group

class Usuario(User):
    """
    Modelo para estender o usuário padrão do Django com informações adicionais.
    """
    biografia = models.TextField(verbose_name="Biografia", blank=True, null=True)
    data_nascimento = models.DateField(verbose_name="Data de Nascimento", blank=True, null=True)
    
    group = models.ForeignKey(
        Group,
        verbose_name='grupo',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        help_text='O grupo a que este usuário pertence. Um usuário terá todas as permissões concedidas a este grupo.',
        related_name="usuarios",
        related_query_name="usuario",
    )

    class Meta:
        verbose_name = "Perfil do Usuário"
        verbose_name_plural = "Perfis dos Usuários"

    def __str__(self):
        return self.username
