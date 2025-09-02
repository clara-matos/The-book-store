from django.urls import path
from . import views

app_name = 'generos'

urlpatterns = [
    path('', views.genero_list, name='lista'),
]
