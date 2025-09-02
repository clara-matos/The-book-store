from django.urls import path
from . import views

app_name = 'autores'

urlpatterns = [
    path('', views.lista_autores, name='lista'),
    path('autor/<int:autor_id>/', views.autor_detalhe, name='detalhe'),
]
