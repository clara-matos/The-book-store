from django.db import models
from autores.models import Autor
from generos.models import Genero
from usuarios.models import PerfilUsuario

class Livro(models.Model):
    """
    Modelo para representar os livros na biblioteca.
    """
    titulo = models.CharField(max_length=255, verbose_name="Título")
    autor = models.ForeignKey(Autor, on_delete=models.CASCADE, related_name='livros')
    genero = models.ForeignKey(Genero, on_delete=models.SET_NULL, related_name='livros', blank=True, null=True)
    lido = models.BooleanField(default=False, verbose_name="Lido")
    usuario = models.ForeignKey(PerfilUsuario, on_delete=models.SET_NULL, related_name='minha_biblioteca', blank=True, null=True)
    capa = models.ImageField(upload_to='livros/capas/', blank=True, null=True, verbose_name="Capa do Livro")

    class Meta:
        verbose_name = "Livro"
        verbose_name_plural = "Livros"

    def __str__(self):
        return self.titulo
