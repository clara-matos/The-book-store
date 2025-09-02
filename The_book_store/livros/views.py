from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .models import Livro, Autor, Genero
from .forms import LivroForm # Precisamos criar este formulário em um arquivo `forms.py`

def listar_livros(request):
    """
    Exibe uma lista de todos os livros.
    Equivale à função `index` do seu urls.py.
    """
    livros = Livro.objects.all()
    context = {'livros': livros}
    return render(request, 'livros/index.html', context)

def livro_detalhe(request, pk):
    """
    Exibe os detalhes de um único livro.
    """
    livro = get_object_or_404(Livro, pk=pk)
    context = {'livro': livro}
    return render(request, 'livros/livro_detalhe.html', context)

def adicionar_livro(request):
    """
    Permite a criação de um novo livro.
    """
    if request.method == 'POST':
        form = LivroForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('livros:home'))
    else:
        form = LivroForm()
    
    context = {'form': form}
    return render(request, 'livros/adicionar_livro.html', context)

def editar_livro(request, pk):
    """
    Permite a atualização de um livro existente.
    """
    livro = get_object_or_404(Livro, pk=pk)
    if request.method == 'POST':
        form = LivroForm(request.POST, instance=livro)
        if form.is_valid():
            form.save()
            return redirect(reverse('livros:home'))
    else:
        form = LivroForm(instance=livro)
        
    context = {'form': form}
    return render(request, 'livros/editar_livro.html', context)

def deletar_livro(request, pk):
    """
    Permite a exclusão de um livro.
    """
    livro = get_object_or_404(Livro, pk=pk)
    if request.method == 'POST':
        livro.delete()
        return redirect(reverse('livros:home'))
        
    context = {'livro': livro}
    return render(request, 'livros/deletar_livro.html', context)
