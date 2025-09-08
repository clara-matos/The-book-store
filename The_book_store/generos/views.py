from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .models import Genero
from .forms import GeneroForm
from django.contrib.auth.decorators import login_required, permission_required

@login_required
def genero_list(request):
    """
    Exibe uma lista de todos os gêneros.
    """
    generos = Genero.objects.all()
    context = {'generos': generos}
    return render(request, 'generos/genero_list.html', context)

@login_required
def genero_detalhe(request, pk):
    """
    Exibe os detalhes de um único gênero.
    """
    genero = get_object_or_404(Genero, pk=pk)
    context = {'genero': genero}
    return render(request, 'generos/genero_detalhe.html', context)

@login_required
@permission_required('generos.add_genero', raise_exception=True)
def adicionar_genero(request):
    """
    Permite a criação de um novo gênero.
    """
    if request.method == 'POST':
        form = GeneroForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('generos:lista_generos'))
    else:
        form = GeneroForm()
    
    context = {'form': form}
    return render(request, 'generos/genero_form.html', context)

@login_required
@permission_required('generos.change_genero', raise_exception=True)
def editar_genero(request, pk):
    """
    Permite a atualização de um gênero existente.
    """
    genero = get_object_or_404(Genero, pk=pk)
    if request.method == 'POST':
        form = GeneroForm(request.POST, instance=genero)
        if form.is_valid():
            form.save()
            return redirect(reverse('generos:lista_generos'))
    else:
        form = GeneroForm(instance=genero)
        
    context = {'form': form}
    return render(request, 'generos/genero_form.html', context)

@login_required
@permission_required('generos.delete_genero', raise_exception=True)
def deletar_genero(request, pk):
    """
    Permite a exclusão de um gênero.
    """
    genero = get_object_or_404(Genero, pk=pk)
    if request.method == 'POST':
        genero.delete()
        return redirect(reverse('generos:lista_generos'))
        
    context = {'genero': genero}
    return render(request, 'generos/genero_confirm_delete.html', context)
