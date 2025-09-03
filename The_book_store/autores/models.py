from django.db import models
from django.urls import reverse
from generos.models import Genero  

class Autor(models.Model):
    nome = models.CharField(max_length=200)
    pais = models.CharField(max_length=100, blank=True, null=True)
    data_nascimento = models.DateField(blank=True, null=True)
    data_falecimento = models.DateField(blank=True, null=True)
    biografia = models.TextField(blank=True, null=True)
    generos = models.ManyToManyField(
        Genero, 
        related_name='autores', 
        blank=True,
        verbose_name="Gêneros literários"
    )
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.nome
    
    def get_absolute_url(self):
        return reverse('autores:autor_detalhe', kwargs={'pk': self.pk})
    
    @property
    def generos_principais(self):
        """Retorna os gêneros mais comuns nos livros do autor"""
        from django.db.models import Count
        return Genero.objects.filter(livro__autores=self).annotate(
            total_livros=Count('livro')
        ).distinct().order_by('-total_livros')[:5]
    
    class Meta:
        verbose_name = "Autor"
        verbose_name_plural = "Autores"
        ordering = ['nome']