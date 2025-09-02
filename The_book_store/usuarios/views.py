from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

@login_required
def perfil(request):
    """
    Exibe a página de perfil do usuário.
    Requer que o usuário esteja logado.
    """
    return render(request, 'usuarios/perfil.html')

def registro(request):
    """
    Permite que novos usuários se registrem.
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')  # Redireciona para a página inicial após o registro
    else:
        form = UserCreationForm()
    
    return render(request, 'usuarios/registro.html', {'form': form})
