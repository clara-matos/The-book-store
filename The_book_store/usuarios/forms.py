from django import forms
from django.contrib.auth.models import Group
from .models import Usuario

class UsuarioForm(forms.ModelForm):
    """
    Um formulário para a criação e edição do perfil do usuário.
    Permite a associação a um grupo, exceto o grupo 'Administradores'.
    """
    group = forms.ModelChoiceField(
        queryset=Group.objects.exclude(name='Administradores'),
        required=False,
        help_text='O grupo a que este usuário pertence.'
    )
    
    class Meta:
        model = Usuario
        fields = ('biografia', 'data_nascimento', 'group')
        widgets = {
            'biografia': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Conte um pouco sobre você...'}),
            'data_nascimento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
