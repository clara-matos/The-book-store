from django.db import models
from livros.models import Livro
from usuarios.models import Usuario

class NotaDeLeitura(models.Model):
    """
    Modelo para armazenar notas e comentários de um livro por um usuário.
    """
    livro = models.ForeignKey(Livro, on_delete=models.CASCADE, related_name='notas')
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='notas_de_leitura')
    comentario = models.TextField(verbose_name="Comentário")
    data = models.DateField(auto_now_add=True, verbose_name="Data da Nota")

    class Meta:
        verbose_name = "Nota de Leitura"
        verbose_name_plural = "Notas de Leitura"
        unique_together = ('livro', 'usuario',)

    def __str__(self):
        return f"Nota de {self.usuario.username} para '{self.livro.titulo}'"
