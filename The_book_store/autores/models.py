from django.db import models

class Autor(models.Model):
    """
    Modelo para representar os autores dos livros.
    """
    nome = models.CharField(max_length=100, verbose_name="Nome")
    pais = models.CharField(max_length=100, verbose_name="País", blank=True, null=True)
    biografia = models.TextField(verbose_name="Biografia", blank=True, null=True)

    class Meta:
        verbose_name = "Autor"
        verbose_name_plural = "Autores"

    def __str__(self):
        return self.nome
