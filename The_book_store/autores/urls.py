from django.urls import path
from . import views

app_name = 'autores'

urlpatterns = [
    path('', views.autor_list, name='autor_list'),
    path('adicionar/', views.adicionar_autor, name='adicionar_autor'),
    path('<int:pk>/', views.autor_detalhe, name='autor_detalhe'),
    path('<int:pk>/editar/', views.editar_autor, name='editar_autor'),
    path('<int:pk>/deletar/', views.deletar_autor, name='deletar_autor'),
]