from django.urls import path
from . import views

app_name = 'notas'

urlpatterns = [
    path('', views.nota_list, name='lista'),
    path('detalhe/<int:pk>/', views.nota_detalhe, name='detalhe'),
    path('adicionar/livro/<int:livro_id>/', views.adicionar_nota, name='adicionar_para_livro'),
    path('editar/<int:pk>/', views.editar_nota, name='editar'),
    path('deletar/<int:pk>/', views.deletar_nota, name='deletar'),
    path('livro/<int:livro_id>/', views.nota_list_por_livro, name='lista_por_livro'),
]