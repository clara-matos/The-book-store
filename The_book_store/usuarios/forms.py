from django import forms
from .models import Usuario

class UsuarioForm(forms.ModelForm):
    """
    Formulário para a criação e edição do perfil do usuário.
    """
    class Meta:
        model = Usuario
        fields = ('biografia', 'data_nascimento')
        widgets = {
            'biografia': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Conte um pouco sobre você...'}),
            'data_nascimento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
