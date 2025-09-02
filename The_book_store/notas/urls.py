from django.urls import path
from . import views

app_name = 'notas'

urlpatterns = [
    path('livro/<int:livro_id>/', views.notas_livro, name='lista'),
    path('adicionar/', views.adicionar_nota, name='adicionar'),
]