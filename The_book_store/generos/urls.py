from django.urls import path
from . import views

app_name = 'generos'

urlpatterns = [
    path('', views.genero_list, name='lista_generos'),
    path('<int:pk>/', views.genero_detalhe, name='detalhe_genero'),
    path('adicionar/', views.adicionar_genero, name='adicionar_genero'),
    path('editar/<int:pk>/', views.editar_genero, name='editar_genero'),
    path('deletar/<int:pk>/', views.deletar_genero, name='deletar_genero'),
]