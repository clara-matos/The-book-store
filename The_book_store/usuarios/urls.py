from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'usuarios'

urlpatterns = [
    path('perfil/', views.perfil, name='perfil'),
    path('registro/', views.registro, name='registro'),
    path('editar_perfil/', views.editar_perfil, name='editar_perfil'),
    path('login/', auth_views.LoginView.as_view(template_name='usuarios/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
