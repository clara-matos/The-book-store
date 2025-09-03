from django import forms
from .models import Autor
from generos.models import Genero

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
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'pais': forms.TextInput(attrs={'class': 'form-control'}),
            'data_nascimento': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'data_falecimento': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'biografia': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'generos': forms.CheckboxSelectMultiple()
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

        # Aplica classes Bootstrap aos checkboxes de gêneros
        for checkbox in self.fields['generos'].choices:
            self.fields['generos'].widget.attrs.update({'class': 'form-check-input'})

    def clean(self):
        cleaned_data = super().clean()
        nascimento = cleaned_data.get('data_nascimento')
        falecimento = cleaned_data.get('data_falecimento')

        if nascimento and falecimento and falecimento < nascimento:
            self.add_error('data_falecimento', "A data de falecimento não pode ser anterior à data de nascimento.")
