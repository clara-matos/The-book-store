from django.shortcuts import render

def index(request):
    """
    Função de view para a página inicial do projeto, que exibe a lista de livros.
    """
    return render(request, 'livros/index.html')
