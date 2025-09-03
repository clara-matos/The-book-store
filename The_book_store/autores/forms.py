from django import forms
from .models import Autor
from genero.models import Genero

class AutorForm(forms.ModelForm):
    generos = forms.ModelMultipleChoiceField(
        queryset=Genero.objects.all().order_by('nome'),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Gêneros literários associados"
    )
    
    class Meta:
        model = Autor
        fields = [
            'nome', 'pais', 'data_nascimento', 'data_falecimento', 
            'biografia', 'generos'
        ]
        widgets = {
            'data_nascimento': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'data_falecimento': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'pais': forms.TextInput(attrs={'class': 'form-control'}),
            'biografia': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }
        labels = {
            'nome': 'Nome completo',
            'pais': 'País de origem',
            'data_nascimento': 'Data de nascimento',
            'data_falecimento': 'Data de falecimento (se aplicável)',
            'biografia': 'Biografia',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Organiza os gêneros em categorias se necessário
        self.fields['generos'].widget.attrs.update({'class': 'form-check-input'})