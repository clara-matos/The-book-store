from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import NotaDeLeitura
from .forms import NotaDeLeituraForm # Precisamos criar este formulário em um arquivo `forms.py`

# Views para a app Notas usando funções

@login_required
def nota_list(request):
    """
    Exibe uma lista das notas de leitura do usuário logado.
    """
    # Garante que apenas as notas do usuário logado sejam exibidas
    notas = NotaDeLeitura.objects.filter(usuario=request.user)
    context = {'notas': notas}
    return render(request, 'notas/nota_list.html', context)

@login_required
def nota_detalhe(request, pk):
    """
    Exibe os detalhes de uma única nota.
    """
    nota = get_object_or_404(NotaDeLeitura, pk=pk, usuario=request.user)
    context = {'nota': nota}
    return render(request, 'notas/nota_detalhe.html', context)

@login_required
def adicionar_nota(request):
    """
    Permite a criação de uma nova nota.
    """
    if request.method == 'POST':
        form = NotaDeLeituraForm(request.POST)
        if form.is_valid():
            nota = form.save(commit=False)
            nota.usuario = request.user  # Vincula a nota ao usuário logado
            nota.save()
            return redirect(reverse('notas:nota_list'))
    else:
        form = NotaDeLeituraForm()
    
    context = {'form': form}
    return render(request, 'notas/nota_form.html', context)

@login_required
def editar_nota(request, pk):
    """
    Permite a atualização de uma nota existente.
    """
    nota = get_object_or_404(NotaDeLeitura, pk=pk, usuario=request.user)
    if request.method == 'POST':
        form = NotaDeLeituraForm(request.POST, instance=nota)
        if form.is_valid():
            form.save()
            return redirect(reverse('notas:nota_list'))
    else:
        form = NotaDeLeituraForm(instance=nota)
        
    context = {'form': form}
    return render(request, 'notas/nota_form.html', context)

@login_required
def deletar_nota(request, pk):
    """
    Permite a exclusão de uma nota.
    """
    nota = get_object_or_404(NotaDeLeitura, pk=pk, usuario=request.user)
    if request.method == 'POST':
        nota.delete()
        return redirect(reverse('notas:nota_list'))
        
    context = {'nota': nota}
    return render(request, 'notas/nota_confirm_delete.html', context)
