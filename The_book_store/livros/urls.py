from django.urls import path
from . import views

app_name = 'livros'

urlpatterns = [
    path('', views.listar_livros, name='lista_livros'),
    path('<int:pk>/', views.livro_detalhe, name='detalhe_livro'),
    path('adicionar/', views.adicionar_livro, name='adicionar_livro'),
    path('editar/<int:pk>/', views.editar_livro, name='editar_livro'),
    path('deletar/<int:pk>/', views.deletar_livro, name='deletar_livro'),
    path('adicionar-a-lista/<int:pk>/', views.adicionar_a_lista, name='adicionar_a_lista'),
    path('marcar-lido/<int:pk>/', views.marcar_como_lido, name='marcar_como_lido'),
]
