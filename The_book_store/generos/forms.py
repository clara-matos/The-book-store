from django import forms
from .models import Genero

class GeneroForm(forms.ModelForm):
    """
    Formulário para a criação e edição de gêneros.
    """
    class Meta:
        model = Genero
        fields = ['nome', 'descricao']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome do Gênero'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Descrição detalhada do gênero'}),
        }
