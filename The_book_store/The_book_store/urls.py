from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # A rota raiz ('') agora inclui as URLs da app livros
    path('', include('livros.urls')),
    
    # Incluindo as URLs das demais apps
    path('autores/', include('autores.urls')),
    path('generos/', include('generos.urls')),
    path('notas/', include('notas.urls')),
    path('usuarios/', include('usuarios.urls')),
]