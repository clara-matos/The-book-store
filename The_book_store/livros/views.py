from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.urls import reverse
from .models import Livro, Autor, Genero
from .forms import LivroForm
from django.contrib import messages
from notas.models import NotaDeLeitura


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

    # Verificar se o usuário atual já tem uma nota para este livro
    user_has_nota = False
    
    if request.user.is_authenticated:
        # Checa se o usuário tem um perfil associado
        try:
            perfil = request.user.perfil
        except AttributeError:
            messages.error(request, "Perfil de usuário não encontrado. Por favor, complete seu perfil.")
            perfil = None
            
        if perfil:
            user_has_nota = NotaDeLeitura.objects.filter(
                livro=livro,
                usuario=perfil
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
def adicionar_livro(request):
    """
    Permite a criação de um novo livro.
    """
    if request.method == 'POST':
        form = LivroForm(request.POST)
        if form.is_valid():
            livro = form.save(commit=False)
            livro.usuario = request.user.perfil
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
def adicionar_a_lista(request, pk):
    livro = get_object_or_404(Livro, pk=pk)
    
    # Adicionei esta verificação para garantir que o usuário tenha um perfil
    try:
        perfil = request.user.perfil
    except AttributeError:
        messages.error(request, "Perfil de usuário não encontrado. Por favor, complete seu perfil.")
        return redirect(request.META.get('HTTP_REFERER', 'livros:lista_livros'))
    
    # Verificar se o usuário já tem este livro em sua lista
    if livro.usuario and livro.usuario == perfil:
        # Remover da lista
        livro.usuario = None
        livro.lido = False
        messages.info(request, f'"{livro.titulo}" removido da sua lista.')
    else:
        # Adicionar à lista
        livro.usuario = perfil
        livro.lido = False # Define como não lido por padrão ao adicionar
        messages.success(request, f'"{livro.titulo}" adicionado à sua lista!')

    livro.save()

    # Redirecionar de volta para a página de onde veio
    return redirect(request.META.get('HTTP_REFERER', 'livros:lista'))


@login_required
def marcar_como_lido(request, pk):
    livro = get_object_or_404(Livro, pk=pk)

    # Adicionei esta verificação para garantir que o usuário tenha um perfil
    try:
        perfil = request.user.perfil
    except AttributeError:
        messages.error(request, "Perfil de usuário não encontrado. Por favor, complete seu perfil.")
        return redirect('livros:detalhe_livro', pk=livro.pk)

    # Redirecionar de volta para a página de detalhes do livro
    return redirect('livros:detalhe_livro', pk=livro.pk)
