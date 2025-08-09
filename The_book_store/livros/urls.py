from django.urls import path
from . import views

app_name = 'livros'

urlpatterns = [
    path('', views.index, name='index'),
]