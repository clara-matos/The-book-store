from django import forms
from .models import Livro

class LivroForm(forms.ModelForm):
    """
    Formulário para a criação e edição de livros.
    """
    class Meta:
        model = Livro
        fields = ['titulo', 'autor', 'genero', 'lido', 'usuario', 'capa']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite o título do livro'}),
            'autor': forms.Select(attrs={'class': 'form-control'}),
            'genero': forms.Select(attrs={'class': 'form-control'}),
            'lido': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'usuario': forms.Select(attrs={'class': 'form-control'}),
            'capa': forms.FileInput(attrs={'class': 'form-control'}),
        }
