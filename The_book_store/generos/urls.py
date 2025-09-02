from django.urls import path
from . import views

app_name = 'generos'

urlpatterns = [
    path('', views.lista_generos, name='lista'),
]
