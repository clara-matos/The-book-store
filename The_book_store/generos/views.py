from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .models import Genero
from .forms import GeneroForm # Importando o formulário para a criação/edição

# Views para a app Generos usando funções

def genero_list(request):
    """
    Exibe uma lista de todos os gêneros.
    """
    generos = Genero.objects.all()
    context = {'generos': generos}
    return render(request, 'generos/genero_list.html', context)

def genero_detalhe(request, pk):
    """
    Exibe os detalhes de um único gênero.
    """
    genero = get_object_or_404(Genero, pk=pk)
    context = {'genero': genero}
    return render(request, 'generos/genero_detalhe.html', context)

def adicionar_genero(request):
    """
    Permite a criação de um novo gênero.
    """
    if request.method == 'POST':
        form = GeneroForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('generos:genero_list'))
    else:
        form = GeneroForm()
    
    context = {'form': form}
    return render(request, 'generos/genero_form.html', context)

def editar_genero(request, pk):
    """
    Permite a atualização de um gênero existente.
    """
    genero = get_object_or_404(Genero, pk=pk)
    if request.method == 'POST':
        form = GeneroForm(request.POST, instance=genero)
        if form.is_valid():
            form.save()
            return redirect(reverse('generos:genero_list'))
    else:
        form = GeneroForm(instance=genero)
        
    context = {'form': form}
    return render(request, 'generos/genero_form.html', context)

def deletar_genero(request, pk):
    """
    Permite a exclusão de um gênero.
    """
    genero = get_object_or_404(Genero, pk=pk)
    if request.method == 'POST':
        genero.delete()
        return redirect(reverse('generos:genero_list'))
        
    context = {'genero': genero}
    return render(request, 'generos/genero_confirm_delete.html', context)
