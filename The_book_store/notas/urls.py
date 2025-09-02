from django.urls import path
from . import views

app_name = 'notas'

urlpatterns = [
    path('livro/<int:livro_id>/', views.nota_list, name='lista'),
    path('adicionar/', views.adicionar_nota, name='adicionar'),
]