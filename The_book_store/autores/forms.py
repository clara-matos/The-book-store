from django import forms
from .models import Autor

class AutorForm(forms.ModelForm):
    """
    Formulário para a criação e edição de autores.
    """
    class Meta:
        model = Autor
        fields = ['nome', 'pais', 'biografia']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome completo do autor'}),
            'pais': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'País de origem'}),
            'biografia': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Conte um pouco sobre o autor...'}),
        }
