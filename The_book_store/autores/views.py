from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .models import Autor
from .forms import AutorForm # Precisamos criar este formulário em um arquivo `forms.py`


def autor_list(request):
    """
    Exibe uma lista de todos os autores.
    """
    autores = Autor.objects.all()
    context = {'autores': autores}
    return render(request, 'autores/autor_list.html', context)

def autor_detalhe(request, pk):
    """
    Exibe os detalhes de um único autor.
    """
    autor = get_object_or_404(Autor, pk=pk)
    context = {'autor': autor}
    return render(request, 'autores/autor_detalhe.html', context)

def adicionar_autor(request):
    """
    Permite a criação de um novo autor.
    """
    if request.method == 'POST':
        form = AutorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('autores:autor_list'))
    else:
        form = AutorForm()
    
    context = {'form': form}
    return render(request, 'autores/autor_form.html', context)

def editar_autor(request, pk):
    """
    Permite a atualização de um autor existente.
    """
    autor = get_object_or_404(Autor, pk=pk)
    if request.method == 'POST':
        form = AutorForm(request.POST, instance=autor)
        if form.is_valid():
            form.save()
            return redirect(reverse('autores:autor_list'))
    else:
        form = AutorForm(instance=autor)
        
    context = {'form': form}
    return render(request, 'autores/autor_form.html', context)

def deletar_autor(request, pk):
    """
    Permite a exclusão de um autor.
    """
    autor = get_object_or_404(Autor, pk=pk)
    if request.method == 'POST':
        autor.delete()
        return redirect(reverse('autores:autor_list'))
        
    context = {'autor': autor}
    return render(request, 'autores/autor_confirm_delete.html', context)
