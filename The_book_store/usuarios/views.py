from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def perfil(request):
    """
    Exibe a página de perfil do usuário.
    Requer que o usuário esteja logado.
    """
    return render(request, 'usuarios/perfil.html')
