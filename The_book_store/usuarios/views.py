from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .forms import UsuarioForm
from django.contrib import messages
from livros.models import Livro
from notas.models import NotaDeLeitura
from .models import Usuario
from django.urls import reverse


@login_required
@permission_required('usuario.view_usuario', raise_exception=True)
def perfil(request):
    """
    Exibe a página de perfil do usuário.
    Requer que o usuário esteja logado.
    """
    # Como Usuario agora herda de User, podemos usar request.user diretamente.
    usuario_logado = request.user
    livros_na_lista = Livro.objects.filter(usuario=usuario_logado)
    user_notas = NotaDeLeitura.objects.filter(usuario=usuario_logado)

    context = {
        'livros_na_lista': livros_na_lista,
        'user_notas': user_notas,
    }

    return render(request, 'usuarios/perfil.html', context)


@login_required
@permission_required('usuario.view_usuario', raise_exception=True)
def lista_usuarios(request):
    """
    Exibe uma lista de todos os usuários.
    Requer que o usuário esteja logado e tenha permissão de visualização.
    """
    usuarios = Usuario.objects.all().order_by('username')
    context = {'usuarios': usuarios}
    return render(request, 'usuarios/lista.html', context)


@permission_required('usuario.add_usuario', raise_exception=True)
def registro(request):
    """
    Permite que novos usuários se registrem.
    Após o registro, redireciona para a edição do perfil.
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # A classe UserCreationForm cria uma instância do AUTH_USER_MODEL, que é Usuario.
            user = form.save()

            # Faz login automático
            login(request, user)

            # Redireciona para a página de edição do perfil
            return redirect(reverse('usuarios:editar_perfil'))
    else:
        form = UserCreationForm()

    return render(request, 'usuarios/registro.html', {'form': form})


@login_required
@permission_required('usuario.change_usuario', raise_exception=True)
def editar_perfil(request):
    """
    Permite que o usuário edite seu perfil.
    """
    # Usamos request.user diretamente.
    usuario = request.user

    if request.method == 'POST':
        form = UsuarioForm(request.POST, request.FILES, instance=usuario)
        if form.is_valid():
            form.save()
            messages.success(request, 'Seu perfil foi atualizado com sucesso!')
            return redirect('usuarios:perfil')
    else:
        form = UsuarioForm(instance=usuario)

    context = {'form': form}
    return render(request, 'usuarios/editar_perfil.html', context)


@login_required
@permission_required('usuario.delete_usuario', raise_exception=True)
def deletar_perfil(request):
    """
    Permite que o usuário exclua seu próprio perfil.
    """
    # Usamos request.user diretamente.
    usuario = request.user

    if request.method == 'POST':
        # Ao deletar o usuário, o perfil é automaticamente deletado por causa do on_delete=models.CASCADE.
        usuario.delete()
        messages.success(request, "Seu perfil e conta foram excluídos com sucesso.")
        return redirect('livros:lista_livros')
    context = {'usuario': usuario}
    return render(request, 'usuarios/deletar_perfil.html', context)
