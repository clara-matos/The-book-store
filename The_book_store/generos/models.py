from django.db import models

class Genero(models.Model):
    """
    Modelo para representar os gêneros literários.
    """
    nome = models.CharField(max_length=100, verbose_name="Nome")
    descricao = models.TextField(verbose_name="Descrição", blank=True, null=True)

    class Meta:
        verbose_name = "Gênero"
        verbose_name_plural = "Gêneros"

    def __str__(self):
        return self.nome
