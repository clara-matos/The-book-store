from django import forms
from .models import NotaDeLeitura

class NotaDeLeituraForm(forms.ModelForm):
    class Meta:
        model = NotaDeLeitura
        fields = ['comentario']
        widgets = {
            'comentario': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 6,
                'placeholder': 'Compartilhe seus pensamentos sobre o livro...',
            })
        }
        labels = {
            'comentario': 'Sua Nota'
        }