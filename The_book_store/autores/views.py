from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from .models import Autor
from .forms import AutorForm

def autor_list(request):
    """
    Exibe uma lista de todos os autores.
    """
    autores = Autor.objects.prefetch_related('generos').order_by('nome')
    
    # Filtro por gênero
    genero_id = request.GET.get('genero')
    if genero_id:
        autores = autores.filter(generos__id=genero_id)
    
    # Filtro por busca
    search = request.GET.get('search')
    if search:
        autores = autores.filter(
            models.Q(nome__icontains=search) |
            models.Q(pais__icontains=search) |
            models.Q(generos__nome__icontains=search)
        ).distinct()
    
    # Obter todos os gêneros para o filtro
    from genero.models import Genero
    todos_generos = Genero.objects.all().order_by('nome')
    
    context = {
        'autores': autores,
        'todos_generos': todos_generos
    }
    return render(request, 'autores/autor_list.html', context)

def autor_detalhe(request, pk):
    """
    Exibe os detalhes de um único autor.
    """
    autor = get_object_or_404(Autor, pk=pk)
    
    # Obter livros do autor
    livros = autor.livros.all().prefetch_related('generos')
    
    # Obter gêneros principais através dos livros (se não tiver generos diretos)
    generos_principais = []
    if not autor.generos.exists():
        generos_principais = autor.generos_principais
    
    context = {
        'autor': autor,
        'livros': livros,
        'generos_principais': generos_principais
    }
    return render(request, 'autores/autor_detalhe.html', context)

@login_required
@permission_required('autores.add_autor', raise_exception=True)
def adicionar_autor(request):
    """
    Permite a criação de um novo autor.
    """
    if request.method == 'POST':
        form = AutorForm(request.POST)
        if form.is_valid():
            autor = form.save()
            messages.success(request, f'Autor "{autor.nome}" criado com sucesso!')
            return redirect(reverse('autores:autor_detalhe', kwargs={'pk': autor.pk}))
    else:
        form = AutorForm()
    
    context = {'form': form}
    return render(request, 'autores/autor_form.html', context)

@login_required
@permission_required('autores.change_autor', raise_exception=True)
def editar_autor(request, pk):
    """
    Permite a atualização de um autor existente.
    """
    autor = get_object_or_404(Autor, pk=pk)
    
    if request.method == 'POST':
        form = AutorForm(request.POST, instance=autor)
        if form.is_valid():
            autor = form.save()
            messages.success(request, f'Autor "{autor.nome}" atualizado com sucesso!')
            return redirect(reverse('autores:autor_detalhe', kwargs={'pk': autor.pk}))
    else:
        form = AutorForm(instance=autor)
        
    context = {'form': form, 'autor': autor}
    return render(request, 'autores/autor_form.html', context)

@login_required
@permission_required('autores.delete_autor', raise_exception=True)
def deletar_autor(request, pk):
    """
    Permite a exclusão de um autor.
    """
    autor = get_object_or_404(Autor, pk=pk)
    
    if request.method == 'POST':
        nome_autor = autor.nome
        autor.delete()
        messages.success(request, f'Autor "{nome_autor}" excluído com sucesso!')
        return redirect(reverse('autores:autor_list'))
        
    context = {'autor': autor}
    return render(request, 'autores/autor_confirm_delete.html', context)