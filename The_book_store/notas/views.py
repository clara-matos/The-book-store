from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.urls import reverse
from .models import NotaDeLeitura
from .forms import NotaDeLeituraForm
from livros.models import Livro


@login_required
def nota_list(request):
    """
    Exibe uma lista das notas de leitura do usuário logado.
    """
    notas = NotaDeLeitura.objects.filter(usuario=request.user).select_related('livro', 'livro__autor')
    context = {'notas': notas}
    return render(request, 'notas/nota_list.html', context)


@login_required
def nota_detalhe(request, pk):
    """
    Exibe os detalhes de uma única nota.
    """
    nota = get_object_or_404(NotaDeLeitura.objects.select_related('livro', 'livro__autor'), 
                             pk=pk, usuario=request.user)
    context = {'nota': nota}
    return render(request, 'notas/nota_detalhe.html', context)


@login_required
def adicionar_nota(request, livro_id):
    """
    Permite a criação de uma nova nota para um livro específico.
    """
    livro = get_object_or_404(Livro, pk=livro_id)
    
    # Verificar se o usuário já tem uma nota para este livro
    nota_existente = NotaDeLeitura.objects.filter(
        livro=livro, 
        usuario=request.user
    ).first()
    
    if request.method == 'POST':
        form = NotaDeLeituraForm(request.POST, instance=nota_existente)
        if form.is_valid():
            try:
                nota = form.save(commit=False)
                nota.livro = livro
                nota.usuario = request.user
                nota.save()
                
                if nota_existente:
                    pass
                else:
                    pass
                
                return redirect('livros:detalhe_livro', pk=livro.pk)
                    
            except IntegrityError:
                pass
    else:
        form = NotaDeLeituraForm(instance=nota_existente)
    
    context = {
        'form': form,
        'livro': livro,
        'modo_edicao': nota_existente is not None
    }
    return render(request, 'notas/nota_form.html', context)


@login_required
@permission_required('notas.change_notadeleitura', raise_exception=True)
def editar_nota(request, pk):
    """
    Permite a atualização de uma nota existente.
    """
    nota = get_object_or_404(NotaDeLeitura.objects.select_related('livro'), 
                             pk=pk, usuario=request.user)
    
    # Verificação de segurança - garantir que o livro existe
    if not nota.livro:
        nota.delete()
        return redirect('notas:lista')
    
    if request.method == 'POST':
        form = NotaDeLeituraForm(request.POST, instance=nota)
        if form.is_valid():
            form.save()
            return redirect('livros:detalhe_livro', pk=nota.livro.pk)
    else:
        form = NotaDeLeituraForm(instance=nota)
    
    context = {
        'form': form,
        'livro': nota.livro,
        'modo_edicao': True
    }
    return render(request, 'notas/nota_form.html', context)


@login_required
@permission_required('notas.delete_notadeleitura', raise_exception=True)
def deletar_nota(request, pk):
    """
    Permite a exclusão de uma nota.
    """
    nota = get_object_or_404(NotaDeLeitura.objects.select_related('livro'), 
                             pk=pk, usuario=request.user)
    
    if request.method == 'POST':
        livro_pk = nota.livro.pk if nota.livro else None
        nota.delete()
        
        if livro_pk:
            return redirect('livros:detalhe_livro', pk=livro_pk)
        else:
            return redirect('notas:lista')
            
    context = {
        'nota': nota
    }
    return render(request, 'notas/nota_confirm_delete.html', context)


@login_required
@permission_required('notas.view_notadeleitura', raise_exception=True)
def nota_list_por_livro(request, livro_id):
    """
    Exibe todas as notas de um livro específico.
    """
    livro = get_object_or_404(Livro, pk=livro_id)
    notas = NotaDeLeitura.objects.filter(livro=livro).select_related('usuario')

    context = {
        'livro': livro,
        'notas': notas
    }
    return render(request, 'notas/nota_list_por_livro.html', context)
