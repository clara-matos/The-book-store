from django.urls import path
from . import views

app_name = 'livros'

urlpatterns = [
    path('', views.index, name='listar_livros'), 
    path('<int:pk>/', views.livro_detalhe, name='detalhe_livro'),
    path('adicionar/', views.adicionar_livro, name='adicionar_livro'),
    path('editar/<int:pk>/', views.editar_livro, name='editar_livro'),
    path('deletar/<int:pk>/', views.deletar_livro, name='deletar_livro'),
]