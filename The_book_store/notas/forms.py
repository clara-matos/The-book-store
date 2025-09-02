from django import forms
from .models import NotaDeLeitura

class NotaDeLeituraForm(forms.ModelForm):
    """
    Formulário para a criação e edição de notas de leitura.
    """
    class Meta:
        model = NotaDeLeitura
        fields = ['livro', 'comentario']
        widgets = {
            'livro': forms.Select(attrs={'class': 'form-control'}),
            'comentario': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Escreva seu comentário aqui...'}),
        }
