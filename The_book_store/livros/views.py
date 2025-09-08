from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.urls import reverse
from .models import Livro, Autor, Genero
from .forms import LivroForm
from notas.models import NotaDeLeitura


def listar_livros(request):
    """
    Exibe uma lista de todos os livros.
    """
    livros = Livro.objects.all()
    context = {'livros': livros}
    return render(request, 'livros/index.html', context)


@permission_required('livros.view_livro', raise_exception=True)
def livro_detalhe(request, pk):
    """
    Exibe os detalhes de um único livro.
    """
    livro = get_object_or_404(Livro, pk=pk)

    # Verificar se o usuário atual já tem uma nota para este livro
    user_has_nota = False
    
    if request.user.is_authenticated:
        user_has_nota = NotaDeLeitura.objects.filter(
            livro=livro,
            usuario=request.user
        ).exists()
            
    # Obter outras informações
    outros_livros = livro.autor.livros.all().exclude(pk=livro.pk)[:4]
    notas = NotaDeLeitura.objects.filter(livro=livro).order_by('-data')

    context = {
        'livro': livro,
        'user_has_nota': user_has_nota,
        'outros_livros': outros_livros,
        'notas': notas,
    }
    return render(request, 'livros/livro_detalhe.html', context)


@login_required
@permission_required('livros.add_livro', raise_exception=True)
def adicionar_livro(request):
    """
    Permite a criação de um novo livro.
    """
    if request.method == 'POST':
        form = LivroForm(request.POST)
        if form.is_valid():
            livro = form.save(commit=False)
            livro.usuario = request.user
            livro.save()
            return redirect(reverse('livros:lista_livros'))
    else:
        form = LivroForm()

    context = {'form': form}
    return render(request, 'livros/adicionar_livro.html', context)


@login_required
@permission_required('livros.change_livro', raise_exception=True)
def editar_livro(request, pk):
    """
    Permite a atualização de um livro existente.
    """
    livro = get_object_or_404(Livro, pk=pk)

    if request.method == 'POST':
        form = LivroForm(request.POST, instance=livro)
        if form.is_valid():
            form.save()
            return redirect(reverse('livros:lista_livros'))
    else:
        form = LivroForm(instance=livro)

    context = {'form': form}
    return render(request, 'livros/editar_livro.html', context)


@login_required
@permission_required('livros.delete_livro', raise_exception=True)
def deletar_livro(request, pk):
    """
    Permite a exclusão de um livro.
    """
    livro = get_object_or_404(Livro, pk=pk)
    
    if request.method == 'POST':
        livro.delete()
        return redirect(reverse('livros:lista_livros'))

    context = {'livro': livro}
    return render(request, 'livros/deletar_livro.html', context)


@login_required
@permission_required('livros.add_livro', raise_exception=True)
def adicionar_a_lista(request, pk):
    livro = get_object_or_404(Livro, pk=pk)
    
    if livro.usuario and livro.usuario == request.user:
        # Remover da lista
        livro.usuario = None
        livro.lido = False
    else:
        # Adicionar à lista
        livro.usuario = request.user
        livro.lido = False # Define como não lido por padrão ao adicionar

    livro.save()

    # Redirecionar de volta para a página de onde veio
    return redirect(request.META.get('HTTP_REFERER', 'livros:lista'))


@login_required
@permission_required('livros.change_livro', raise_exception=True)
def marcar_como_lido(request, pk):
    livro = get_object_or_404(Livro, pk=pk)

    # Redirecionar de volta para a página de detalhes do livro
    return redirect('livros:detalhe_livro', pk=livro.pk)
