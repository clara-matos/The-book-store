from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .forms import PerfilUsuarioForm
from django.contrib import messages
from livros.models import Livro
from notas.models import NotaDeLeitura
from usuarios.models import PerfilUsuario
from django.urls import reverse


@login_required
def perfil(request):
    """
    Exibe a página de perfil do usuário.
    Requer que o usuário esteja logado.
    """
    try:
        perfil_usuario = request.user.perfil
        livros_na_lista = perfil_usuario.minha_biblioteca.all()
        user_notas = NotaDeLeitura.objects.filter(usuario=perfil_usuario)

    except PerfilUsuario.DoesNotExist:
        messages.error(request, "Seu perfil não foi encontrado. Por favor, crie um perfil para continuar.")
        return redirect('livros:lista_livros')

    context = {
        'livros_na_lista': livros_na_lista,
        'user_notas': user_notas,
    }

    return render(request, 'usuarios/perfil.html', context)


def registro(request):
    """
    Permite que novos usuários se registrem.
    Após o registro, redireciona para a edição do perfil.
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()

            # Cria o perfil vinculado ao usuário
            PerfilUsuario.objects.create(user=user)

            # Faz login automático
            login(request, user)

            # Redireciona para a página de edição do perfil
            return redirect(reverse('usuarios:editar_perfil'))
    else:
        form = UserCreationForm()

    return render(request, 'usuarios/registro.html', {'form': form})



@login_required
def editar_perfil(request):
    """
    Permite que o usuário edite seu perfil.
    """
    try:
        perfil_usuario = request.user.perfil
    except PerfilUsuario.DoesNotExist:
        messages.error(request, "Seu perfil não foi encontrado. Por favor, crie um perfil para continuar.")
        return redirect('livros:lista')

    if request.method == 'POST':
        form = PerfilUsuarioForm(request.POST, request.FILES, instance=perfil_usuario)
        if form.is_valid():
            form.save()
            messages.success(request, 'Seu perfil foi atualizado com sucesso!')
            return redirect('usuarios:perfil')
    else:
        form = PerfilUsuarioForm(instance=perfil_usuario)

    context = {'form': form}
    return render(request, 'usuarios/editar_perfil.html', context)


@login_required
def deletar_perfil(request):
    """
    Permite que o usuário exclua seu próprio perfil.
    """
    try:
        perfil_usuario = request.user.perfil
    except PerfilUsuario.DoesNotExist:
        messages.error(request, "Perfil não encontrado.")
        return redirect('usuarios:perfil')

    if request.method == 'POST':
        # Opcional: deletar o usuário também
        user = request.user
        perfil_usuario.delete()
        user.delete()
        messages.success(request, "Seu perfil e conta foram excluídos com sucesso.")
        return redirect('livros:lista_livros')  # ou 'login' ou outra página pública

    context = {'perfil': perfil_usuario}
    return render(request, 'usuarios/deletar_perfil.html', context)