from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # A rota raiz ('') agora inclui as URLs da app livros,
    # onde o caminho principal será a lista de livros
    path('', include('livros.urls')),
    
    # Incluindo as URLs das demais apps com seus próprios prefixos
    path('autores/', include('autores.urls')),
    path('generos/', include('generos.urls')),
    path('notas/', include('notas.urls')),
    path('usuarios/', include('usuarios.urls')),
    
    # URLs para Login e Logout
    path('login/', auth_views.LoginView.as_view(template_name='usuarios/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
]
